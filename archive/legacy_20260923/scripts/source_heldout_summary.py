from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "figure_source"
OUT = ROOT / "results" / "source_heldout_results.json"


def records_without_nan(frame: pd.DataFrame) -> list[dict]:
    clean = frame.astype(object).where(pd.notna(frame), None)
    return clean.to_dict(orient="records")


def main() -> None:
    curves = pd.read_csv(DATA / "figure2_source_heldout_profiles.csv")
    summary = pd.read_csv(DATA / "figure2_endpoint_spans.csv")
    retraining = pd.read_csv(DATA / "figure2_retraining_changes.csv")
    payload = {
        "curve_rows": records_without_nan(curves),
        "endpoint_summary": records_without_nan(summary),
        "source_heldout_intervention_summary": records_without_nan(retraining),
    }
    OUT.write_text(json.dumps(payload, indent=2, allow_nan=False), encoding="utf-8")
    print("Wrote", OUT)


if __name__ == "__main__":
    main()
