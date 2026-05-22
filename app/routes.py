import json
from pathlib import Path
from typing import Any

import bleach
import markdown
from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index() -> str:
    return render_template("index.html")


@main_bp.get("/bond-market")
def bond_market() -> str:
    bond_status = _load_bond_market_status()
    ai_analysis_html = _render_markdown_html(
        bond_status.get("ai_analysis", "No AI evaluation available.")
    )
    return render_template(
        "bond_market.html",
        generated_at=bond_status.get("generated_at"),
        source=bond_status.get("source", "Unknown"),
        fetched_at=bond_status.get("fetched_at"),
        indicators=bond_status.get("indicators", []),
        history_series=bond_status.get("history_series", {}),
        signal_summary=bond_status.get("signal_summary", []),
        data_errors=bond_status.get("errors", []),
        ai_analysis_html=ai_analysis_html,
    )


@main_bp.get("/stock-market")
def stock_market() -> str:
    return render_template("stock_market.html")


@main_bp.get("/real-estate-market")
def real_estate_market() -> str:
    return render_template("real_estate_market.html")


@main_bp.get("/global-market")
def global_market() -> str:
    return render_template("global_market.html")


def _load_bond_market_status() -> dict[str, Any]:
    root = Path(__file__).resolve().parents[1]
    status_path = root / "status" / "bond-market" / "latest.json"

    if not status_path.exists():
        return {
            "source": "Unavailable",
            "indicators": [],
            "errors": [
                "No bond batch status file found. Run `python -m batch.jobs.bond_job` first."
            ],
            "ai_analysis": "No AI evaluation available.",
        }

    with status_path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    snapshot = payload.get("snapshot", {})
    signal_evaluation = payload.get("signal_evaluation", {})
    values = snapshot.get("values", {})
    history = snapshot.get("history", {})
    indicators = []
    for name, details in values.items():
        indicators.append(
            {
                "name": name,
                "value": details.get("value"),
                "series_id": details.get("series_id", ""),
                "date": details.get("date", ""),
            }
        )

    history_series: dict[str, list[dict[str, Any]]] = {}
    for key, details in history.items():
        points = details.get("points", [])
        normalized_points: list[dict[str, Any]] = []
        for point in points:
            normalized_points.append(
                {
                    "date": point.get("date"),
                    "value": point.get("value"),
                }
            )
        history_series[key] = normalized_points

    signal_summary = []
    for signal_name, details in signal_evaluation.items():
        status = str(details.get("status", "unknown"))
        signal_summary.append(
            {
                "name": signal_name,
                "status": status,
                "indication": details.get("indication", ""),
                "light": _status_to_light(status),
            }
        )

    return {
        "generated_at": payload.get("generated_at"),
        "source": snapshot.get("source", "Unknown"),
        "fetched_at": snapshot.get("fetched_at"),
        "indicators": indicators,
        "history_series": history_series,
        "signal_summary": signal_summary,
        "errors": snapshot.get("errors", []),
        "ai_analysis": payload.get("ai_analysis", "No AI evaluation available."),
    }


def _status_to_light(status: str) -> str:
    normalized = status.strip().lower()
    if normalized in {"present", "elevated"}:
        return "red"
    if normalized in {"possible", "watch", "mixed", "uncertain"}:
        return "yellow"
    if normalized in {"not present", "contained", "not obvious", "stable"}:
        return "green"
    return "yellow"


def _render_markdown_html(markdown_text: str) -> str:
    raw_html = markdown.markdown(
        markdown_text,
        extensions=["extra", "sane_lists", "nl2br"],
    )
    allowed_tags = set(bleach.sanitizer.ALLOWED_TAGS).union(
        {
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "p",
            "pre",
            "code",
            "ul",
            "ol",
            "li",
            "strong",
            "em",
            "blockquote",
            "hr",
            "br",
        }
    )
    allowed_attributes = {
        "a": ["href", "title", "rel"],
    }
    return bleach.clean(
        raw_html,
        tags=allowed_tags,
        attributes=allowed_attributes,
        protocols=["http", "https", "mailto"],
        strip=True,
    )
