from __future__ import annotations

import json
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


def evaluate_bond_signals(snapshot: dict[str, Any]) -> dict[str, dict[str, str]]:
    yc = _value(snapshot, "yield_curve_10y_2y")
    y10 = _value(snapshot, "yield_10y")
    hy_spread = _value(snapshot, "high_yield_spread")
    real_yield = _value(snapshot, "real_yield_10y")
    stress = _value(snapshot, "financial_stress_index")
    vol_proxy = _value(snapshot, "market_volatility_proxy")

    signals: dict[str, dict[str, str]] = {
        "Inverted yield curve": {
            "status": "present" if yc is not None and yc < 0 else "not present",
            "indication": "Higher recession risk",
        },
        "Falling long-term yields during stress": {
            "status": (
                "possible" if y10 is not None and stress is not None and y10 < 3.5 and stress > 0.5 else "not obvious"
            ),
            "indication": "Growth fear or flight to safety",
        },
        "Rising long-term yields": {
            "status": "elevated" if y10 is not None and y10 >= 4.5 else "contained",
            "indication": "Inflation concern, fiscal concern, or stronger growth expectations",
        },
        "Widening credit spreads": {
            "status": "elevated" if hy_spread is not None and hy_spread >= 4.5 else "contained",
            "indication": "Rising corporate stress",
        },
        "Rising real yields": {
            "status": "elevated" if real_yield is not None and real_yield >= 1.75 else "contained",
            "indication": "Valuation pressure on stocks",
        },
        "Treasury liquidity stress": {
            "status": (
                "possible" if stress is not None and vol_proxy is not None and stress > 1.0 and vol_proxy > 25 else "not obvious"
            ),
            "indication": "Broader financial-system stress",
        },
    }
    return signals


def format_markdown_report(payload: dict[str, Any], ai_analysis: str) -> str:
    snapshot = payload["snapshot"]
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
    signal_evaluation = evaluate_bond_signals(snapshot)
    payload: dict[str, Any] = {
        "generated_at": datetime.now(UTC).isoformat(),
        "snapshot": snapshot,
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
