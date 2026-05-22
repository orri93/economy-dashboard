from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from openai import OpenAI


class OpenAIMarketEvaluator:
    """Shared OpenAI client wrapper for market evaluation jobs."""

    def __init__(self, model: str | None = None) -> None:
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-5-mini")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def load_instruction_file(self, instruction_path: Path) -> str:
        return instruction_path.read_text(encoding="utf-8")

    def evaluate(self, instruction_text: str, payload: dict[str, Any]) -> str:
        if not self.client:
            return self._fallback_summary(payload)

        try:
            response = self.client.responses.create(
                model=self.model,
                input=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "input_text",
                                "text": instruction_text,
                            }
                        ],
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": (
                                    "Evaluate the latest bond-market state using this JSON payload:\n"
                                    + json.dumps(payload, indent=2)
                                ),
                            }
                        ],
                    },
                ],
            )
            return response.output_text.strip()
        except Exception as exc:
            return self._fallback_summary(payload, reason=f"OpenAI call failed: {exc}")

    def _fallback_summary(self, payload: dict[str, Any], reason: str | None = None) -> str:
        signals = payload.get("signal_evaluation", {})
        lines = [
            "## Bond Market AI Evaluation (Fallback)",
            (
                "OPENAI_API_KEY is not set, so this run used deterministic fallback logic."
                if reason is None
                else f"Deterministic fallback used because: {reason}"
            ),
            "",
        ]
        for signal_name, signal in signals.items():
            status = signal.get("status", "unknown")
            implication = signal.get("indication", "No indication available")
            lines.append(f"- **{signal_name}**: {status}. {implication}")
        return "\n".join(lines)
