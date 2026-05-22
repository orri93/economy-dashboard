from __future__ import annotations

import json
import math
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from batch.common.data_sources import FREDClient, fetch_bond_market_snapshot
from batch.common.openai_processor import OpenAIMarketEvaluator


def _value(snapshot: dict[str, Any], key: str) -> float | None:
    item = snapshot.get("values", {}).get(key)
    if not item:
        return None
    return item.get("value")


def _history_values(snapshot: dict[str, Any], key: str) -> list[float]:
    points = snapshot.get("history", {}).get(key, {}).get("points", [])
    values: list[float] = []
    for point in points:
        value = point.get("value")
        if isinstance(value, (int, float)) and math.isfinite(value):
            values.append(float(value))
    return values


def _lag_value(values: list[float], lag_days: int) -> float | None:
    if len(values) <= lag_days:
        return None
    return values[-(lag_days + 1)]


def _delta(current: float | None, previous: float | None) -> float | None:
    if current is None or previous is None:
        return None
    return round(current - previous, 4)


def _percentile_rank(values: list[float], current: float | None) -> float | None:
    if not values or current is None:
        return None
    less_or_equal = sum(1 for value in values if value <= current)
    return round(100.0 * less_or_equal / len(values), 1)


def build_trend_context(snapshot: dict[str, Any]) -> dict[str, dict[str, float | None]]:
    trend_context: dict[str, dict[str, float | None]] = {}

    for key in snapshot.get("values", {}).keys():
        current = _value(snapshot, key)
        raw_points = snapshot.get("history", {}).get(key, {}).get("points", [])

        dated_points: list[tuple[datetime, float]] = []
        for point in raw_points:
            date_text = point.get("date")
            value = point.get("value")
            if not date_text or not isinstance(value, (int, float)) or not math.isfinite(value):
                continue
            try:
                point_dt = datetime.fromisoformat(str(date_text))
            except ValueError:
                continue
            dated_points.append((point_dt, float(value)))

        dated_points.sort(key=lambda item: item[0])
        values = [value for _, value in dated_points]

        def value_at_or_before(target_dt: datetime) -> float | None:
            for point_dt, value in reversed(dated_points):
                if point_dt <= target_dt:
                    return value
            return None

        prior_30d = None
        prior_1y = None
        if dated_points:
            last_dt = dated_points[-1][0]
            prior_30d = value_at_or_before(datetime.fromordinal(last_dt.toordinal() - 30))
            prior_1y = value_at_or_before(datetime.fromordinal(last_dt.toordinal() - 365))

        trend_context[key] = {
            "current": current,
            "change_30d": _delta(current, prior_30d),
            "change_1y": _delta(current, prior_1y),
            "percentile_1y": _percentile_rank(values, current),
            "sample_size": float(len(values)),
        }

    return trend_context


def evaluate_bond_signals(
    snapshot: dict[str, Any],
    trend_context: dict[str, dict[str, float | None]],
) -> dict[str, dict[str, str]]:
    yc = _value(snapshot, "yield_curve_10y_2y")
    y10 = _value(snapshot, "yield_10y")
    hy_spread = _value(snapshot, "high_yield_spread")
    real_yield = _value(snapshot, "real_yield_10y")

    y10_30d = trend_context.get("yield_10y", {}).get("change_30d")
    y10_pct = trend_context.get("yield_10y", {}).get("percentile_1y")
    hy_30d = trend_context.get("high_yield_spread", {}).get("change_30d")
    hy_pct = trend_context.get("high_yield_spread", {}).get("percentile_1y")
    real_30d = trend_context.get("real_yield_10y", {}).get("change_30d")
    real_pct = trend_context.get("real_yield_10y", {}).get("percentile_1y")
    stress_pct = trend_context.get("financial_stress_index", {}).get("percentile_1y")
    vix_pct = trend_context.get("market_volatility_proxy", {}).get("percentile_1y")

    def has_metric(value: float | None) -> bool:
        return value is not None

    falling_yields_during_stress = (
        has_metric(y10_30d)
        and has_metric(stress_pct)
        and y10_30d <= -0.25
        and cast_float(stress_pct) >= 70
    )
    rising_long_yields = (
        (has_metric(y10_30d) and y10_30d >= 0.25)
        or (has_metric(y10_pct) and cast_float(y10_pct) >= 70)
        or (y10 is not None and y10 >= 4.5)
    )
    widening_credit = (
        (has_metric(hy_30d) and hy_30d >= 0.4)
        or (has_metric(hy_pct) and cast_float(hy_pct) >= 70)
        or (hy_spread is not None and hy_spread >= 4.5)
    )
    rising_real = (
        (has_metric(real_30d) and real_30d >= 0.2)
        or (has_metric(real_pct) and cast_float(real_pct) >= 70)
        or (real_yield is not None and real_yield >= 1.75)
    )
    liquidity_stress = (
        has_metric(stress_pct)
        and has_metric(vix_pct)
        and cast_float(stress_pct) >= 80
        and cast_float(vix_pct) >= 70
    )

    signals: dict[str, dict[str, str]] = {
        "Inverted yield curve": {
            "status": "present" if yc is not None and yc < 0 else "not present",
            "indication": "Higher recession risk",
            "evidence": f"10y-2y current={yc}",
        },
        "Falling long-term yields during stress": {
            "status": "possible" if falling_yields_during_stress else "not obvious",
            "indication": "Growth fear or flight to safety",
            "evidence": f"10y 30d change={y10_30d}, stress percentile={stress_pct}",
        },
        "Rising long-term yields": {
            "status": "elevated" if rising_long_yields else "contained",
            "indication": "Inflation concern, fiscal concern, or stronger growth expectations",
            "evidence": f"10y current={y10}, 10y 30d change={y10_30d}, 10y 1y percentile={y10_pct}",
        },
        "Widening credit spreads": {
            "status": "elevated" if widening_credit else "contained",
            "indication": "Rising corporate stress",
            "evidence": f"HY spread current={hy_spread}, HY 30d change={hy_30d}, HY 1y percentile={hy_pct}",
        },
        "Rising real yields": {
            "status": "elevated" if rising_real else "contained",
            "indication": "Valuation pressure on stocks",
            "evidence": f"Real 10y current={real_yield}, real 30d change={real_30d}, real 1y percentile={real_pct}",
        },
        "Treasury liquidity stress": {
            "status": "possible" if liquidity_stress else "not obvious",
            "indication": "Broader financial-system stress",
            "evidence": f"Stress percentile={stress_pct}, VIX percentile={vix_pct}",
        },
    }
    return signals


def cast_float(value: float | None) -> float:
    return float(value) if value is not None else float("nan")


def format_markdown_report(payload: dict[str, Any], ai_analysis: str) -> str:
    snapshot = payload["snapshot"]
    trend_context = payload.get("trend_context", {})
    lines = [
        "# Bond Market Status",
        "",
        f"- Generated at: {payload['generated_at']}",
        f"- Source: {snapshot.get('source', 'unknown')}",
        "",
        "## Latest Indicators",
    ]

    for indicator, item in snapshot.get("values", {}).items():
        lines.append(
            f"- **{indicator}**: {item['value']} (series `{item['series_id']}`, date {item['date']})"
        )

    if trend_context:
        lines.append("")
        lines.append("## One-Year Trend Context (Calendar Day Deltas; nearest available observation)")
        for indicator, trend in trend_context.items():
            lines.append(
                "- **{name}**: 30d change={c30}, 1y change={c1y}, 1y percentile={pct}, samples={n}".format(
                    name=indicator,
                    c30=trend.get("change_30d"),
                    c1y=trend.get("change_1y"),
                    pct=trend.get("percentile_1y"),
                    n=int(trend.get("sample_size", 0.0)),
                )
            )

    if snapshot.get("errors"):
        lines.append("")
        lines.append("## Data Fetch Notes")
        for err in snapshot["errors"]:
            lines.append(f"- {err}")

    lines.append("")
    lines.append("## Signal Evaluation")
    for signal_name, signal in payload["signal_evaluation"].items():
        lines.append(f"- **{signal_name}**: {signal['status']} -> {signal['indication']}")

    lines.append("")
    lines.append("## OpenAI Assessment")
    lines.append(ai_analysis)
    return "\n".join(lines) + "\n"


def run() -> None:
    root = Path(__file__).resolve().parents[2]
    instruction_path = root / "instructions" / "bond-market-evaluation.md"
    status_dir = root / "status" / "bond-market"
    status_dir.mkdir(parents=True, exist_ok=True)

    snapshot = fetch_bond_market_snapshot(FREDClient())
    trend_context = build_trend_context(snapshot)
    signal_evaluation = evaluate_bond_signals(snapshot, trend_context)
    payload: dict[str, Any] = {
        "generated_at": datetime.now(UTC).isoformat(),
        "snapshot": snapshot,
        "trend_context": trend_context,
        "signal_evaluation": signal_evaluation,
    }

    evaluator = OpenAIMarketEvaluator(model="gpt-5-mini")
    instructions = evaluator.load_instruction_file(instruction_path)
    ai_analysis = evaluator.evaluate(instructions, payload)

    markdown_report = format_markdown_report(payload, ai_analysis)
    latest_md_path = status_dir / "latest.md"
    latest_json_path = status_dir / "latest.json"

    latest_md_path.write_text(markdown_report, encoding="utf-8")
    latest_json_path.write_text(
        json.dumps(
            {
                **payload,
                "ai_analysis": ai_analysis,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"[{datetime.now(UTC).isoformat()}] Bond market batch job completed.")
    print(f"Updated: {latest_md_path}")
    print(f"Updated: {latest_json_path}")


if __name__ == "__main__":
    run()
