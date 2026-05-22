from __future__ import annotations

import csv
import os
from io import StringIO
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

import requests


FRED_BASE_URL = "https://api.stlouisfed.org/fred"


@dataclass
class FREDObservation:
    series_id: str
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
    errors: list[str] = []

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
        except requests.RequestException as exc:
            errors.append(f"Failed to fetch {series_id}: {exc}")

    return {
        "source": "FRED",
        "fetched_at": datetime.now(UTC).isoformat(),
        "values": values,
        "errors": errors,
    }
