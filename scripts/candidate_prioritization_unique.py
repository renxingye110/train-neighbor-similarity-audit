from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "figure_source"
OUT = ROOT / "results" / "candidate_prioritization_results.json"


def main() -> None:
    summary = pd.read_csv(DATA / "figure3_unique_candidate_pool_summary.csv").iloc[0].to_dict()
    raw_top20 = pd.read_csv(DATA / "figure3_raw_top20.csv")
    audited_top20 = pd.read_csv(DATA / "figure3_audited_top20.csv")
    composition = pd.read_csv(DATA / "figure3_similarity_composition.csv")
    replaced = pd.read_csv(DATA / "figure3_replaced_candidates.csv")
    payload = {
        "summary": summary,
        "raw_top20": raw_top20.to_dict(orient="records"),
        "audited_top20": audited_top20.to_dict(orient="records"),
        "composition": composition.to_dict(orient="records"),
        "replaced_candidates": replaced.to_dict(orient="records"),
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("Wrote", OUT)


if __name__ == "__main__":
    main()
