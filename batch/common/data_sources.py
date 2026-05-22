from __future__ import annotations

import csv
import os
from io import StringIO
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from typing import Any

import requests


FRED_BASE_URL = "https://api.stlouisfed.org/fred"


@dataclass
class FREDObservation:
    series_id: str
    date: str
    value: float


@dataclass
class FREDSeriesPoint:
    date: str
    value: float


class FREDClient:
    """Minimal FRED API client for time-series observations."""

    def __init__(self, api_key: str | None = None, timeout: int = 20) -> None:
        self.api_key = api_key or os.getenv("FRED_API_KEY")
        self.timeout = timeout
        self.session = requests.Session()

    def _build_params(self, params: dict[str, Any]) -> dict[str, Any]:
        base = {"file_type": "json"}
        if self.api_key:
            base["api_key"] = self.api_key
        base.update(params)
        return base

    def latest_observation(self, series_id: str) -> FREDObservation | None:
        url = f"{FRED_BASE_URL}/series/observations"
        params = self._build_params(
            {
                "series_id": series_id,
                "sort_order": "desc",
                "limit": 30,
            }
        )
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            observations = response.json().get("observations", [])
            for item in observations:
                value_str = item.get("value", ".")
                if value_str in {".", None, ""}:
                    continue
                try:
                    value = float(value_str)
                except ValueError:
                    continue
                return FREDObservation(series_id=series_id, date=item["date"], value=value)
            return None
        except requests.HTTPError:
            # Fallback for environments without FRED API key: use CSV endpoint.
            return self._latest_observation_from_csv(series_id)

    def observations(
        self,
        series_id: str,
        *,
        start_date: date,
        end_date: date,
    ) -> list[FREDSeriesPoint]:
        url = f"{FRED_BASE_URL}/series/observations"
        params = self._build_params(
            {
                "series_id": series_id,
                "observation_start": start_date.isoformat(),
                "observation_end": end_date.isoformat(),
                "sort_order": "asc",
            }
        )
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            items = response.json().get("observations", [])
            return self._parse_api_points(items)
        except requests.HTTPError:
            return self._observations_from_csv(
                series_id,
                start_date=start_date,
                end_date=end_date,
            )

    def _latest_observation_from_csv(self, series_id: str) -> FREDObservation | None:
        csv_url = "https://fred.stlouisfed.org/graph/fredgraph.csv"
        response = self.session.get(csv_url, params={"id": series_id}, timeout=self.timeout)
        response.raise_for_status()

        rows = list(csv.DictReader(StringIO(response.text)))
        for row in reversed(rows):
            value_str = row.get(series_id, ".")
            if value_str in {".", None, ""}:
                continue
            try:
                value = float(value_str)
            except ValueError:
                continue
            date = (
                row.get("DATE")
                or row.get("date")
                or row.get("observation_date")
                or row.get("\ufeffDATE")
                or ""
            )
            return FREDObservation(series_id=series_id, date=date, value=value)
        return None

    def _observations_from_csv(
        self,
        series_id: str,
        *,
        start_date: date,
        end_date: date,
    ) -> list[FREDSeriesPoint]:
        csv_url = "https://fred.stlouisfed.org/graph/fredgraph.csv"
        response = self.session.get(csv_url, params={"id": series_id}, timeout=self.timeout)
        response.raise_for_status()

        rows = list(csv.DictReader(StringIO(response.text)))
        points: list[FREDSeriesPoint] = []
        for row in rows:
            date_text = (
                row.get("DATE")
                or row.get("date")
                or row.get("observation_date")
                or row.get("\ufeffDATE")
                or ""
            )
            if not date_text:
                continue
            try:
                point_date = date.fromisoformat(date_text)
            except ValueError:
                continue
            if point_date < start_date or point_date > end_date:
                continue
            value = _parse_numeric(row.get(series_id, "."))
            if value is None:
                continue
            points.append(FREDSeriesPoint(date=point_date.isoformat(), value=value))
        return points

    def _parse_api_points(self, items: list[dict[str, Any]]) -> list[FREDSeriesPoint]:
        points: list[FREDSeriesPoint] = []
        for item in items:
            value = _parse_numeric(item.get("value", "."))
            if value is None:
                continue
            point_date = item.get("date")
            if not point_date:
                continue
            points.append(FREDSeriesPoint(date=point_date, value=value))
        return points


def fetch_bond_market_snapshot(client: FREDClient) -> dict[str, Any]:
    """Fetch latest bond-market indicators used by the batch evaluator."""
    # These series are chosen to cover curve shape, nominal and real yields,
    # credit stress, and broad financial-system stress proxies.
    series_map = {
        "yield_curve_10y_2y": "T10Y2Y",
        "yield_2y": "DGS2",
        "yield_10y": "DGS10",
        "yield_30y": "DGS30",
        "real_yield_10y": "DFII10",
        "high_yield_spread": "BAMLH0A0HYM2",
        "baa_10y_spread": "BAA10Y",
        "financial_stress_index": "STLFSI4",
        "financial_conditions_index": "NFCI",
        "market_volatility_proxy": "VIXCLS",
    }

    values: dict[str, dict[str, Any]] = {}
    history: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    end_date = datetime.now(UTC).date()
    start_date = end_date - timedelta(days=365)

    for key, series_id in series_map.items():
        try:
            obs = client.latest_observation(series_id)
            if obs is None:
                errors.append(f"No data returned for series {series_id}")
                continue
            values[key] = {
                "series_id": obs.series_id,
                "date": obs.date,
                "value": obs.value,
            }
            history_points = client.observations(
                series_id,
                start_date=start_date,
                end_date=end_date,
            )
            history[key] = {
                "series_id": series_id,
                "resolution": "daily",
                "from": start_date.isoformat(),
                "to": end_date.isoformat(),
                "points": [
                    {"date": point.date, "value": point.value} for point in history_points
                ],
            }
        except requests.RequestException as exc:
            errors.append(f"Failed to fetch {series_id}: {exc}")

    return {
        "source": "FRED",
        "fetched_at": datetime.now(UTC).isoformat(),
        "history": history,
        "values": values,
        "errors": errors,
    }


def _parse_numeric(raw_value: Any) -> float | None:
    if raw_value in {".", None, ""}:
        return None
    try:
        return float(raw_value)
    except (TypeError, ValueError):
        return None
