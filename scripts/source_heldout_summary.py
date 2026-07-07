from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "figure_source"
OUT = ROOT / "results" / "source_heldout_results.json"


def main() -> None:
    curves = pd.read_csv(DATA / "figure2_source_heldout_profiles.csv")
    summary = pd.read_csv(DATA / "figure2_endpoint_spans.csv")
    retraining = pd.read_csv(DATA / "figure2_retraining_changes.csv")
    payload = {
        "curve_rows": curves.to_dict(orient="records"),
        "endpoint_summary": summary.to_dict(orient="records"),
        "neighbor_removal_summary": retraining.to_dict(orient="records"),
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("Wrote", OUT)


if __name__ == "__main__":
    main()
