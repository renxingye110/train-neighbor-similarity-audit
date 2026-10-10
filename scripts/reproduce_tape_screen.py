from __future__ import annotations

import argparse
import csv
import json
import platform
import sys
from pathlib import Path

import numpy as np
import scipy
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from benchmark_diagnostic import (  # noqa: E402
    build_kmer_matrix,
    diagnose_binary_endpoint,
    map_kmer_matrix,
    top_neighbors,
)


def read_json(path: Path) -> list[dict]:
    rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError(f"Expected a list of records in {path}")
    return rows


def read_reference(path: Path) -> dict[str, dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return {row["endpoint"]: row for row in csv.DictReader(handle)}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Recompute the TAPE remote-homology one-vs-rest screen."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        required=True,
        help="Directory containing the three TAPE remote-homology JSON split files.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=ROOT / "configs" / "released_analysis.json",
    )
    parser.add_argument(
        "--reference-table",
        type=Path,
        default=ROOT / "data" / "tables" / "supp_table_s3_primary_endpoint_screen.csv",
    )
    parser.add_argument(
        "--output-dir", type=Path, required=True, help="Directory for result files"
    )
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    train_records = read_json(args.data_dir / "remote_homology_train.json")
    valid_records = read_json(args.data_dir / "remote_homology_valid.json")
    test_records = read_json(args.data_dir / "remote_homology_test_family_holdout.json")
    training = train_records + valid_records
    train_sequences = [row["primary"].upper() for row in training]
    test_sequences = [row["primary"].upper() for row in test_records]
    train_classes = np.asarray([row["class_label"] for row in training], dtype=np.int32)
    test_classes = np.asarray([row["class_label"] for row in test_records], dtype=np.int32)

    train_matrix, train_lengths, train_counts, token_to_column = build_kmer_matrix(
        train_sequences, int(config["kmer_size"])
    )
    test_matrix, test_lengths, test_counts = map_kmer_matrix(
        test_sequences, token_to_column, int(config["kmer_size"])
    )
    test_neighbors, test_max = top_neighbors(
        test_matrix,
        test_lengths,
        test_counts,
        train_matrix,
        train_lengths,
        train_counts,
        top_k=int(config["top_k"]),
        k=int(config["kmer_size"]),
    )
    _, train_max = top_neighbors(
        train_matrix,
        train_lengths,
        train_counts,
        test_matrix,
        test_lengths,
        test_counts,
        top_k=int(config["top_k"]),
        k=int(config["kmer_size"]),
    )
    clean_train = train_max < float(config["clean_train_threshold"])
    reference = read_reference(args.reference_table)
    rows = []

    for target_class in sorted(np.unique(test_classes)):
        train_y = (train_classes == target_class).astype(np.int8)
        test_y = (test_classes == target_class).astype(np.int8)
        model = LogisticRegression(
            max_iter=int(config["tape_logistic_max_iter"]),
            solver=str(config["tape_logistic_solver"]),
        )
        model.fit(train_matrix.astype(np.float32), train_y)
        fixed_scores = model.predict_proba(test_matrix.astype(np.float32))[:, 1]

        clean_model = LogisticRegression(
            max_iter=int(config["tape_logistic_max_iter"]),
            solver=str(config["tape_logistic_solver"]),
        )
        clean_model.fit(train_matrix[clean_train].astype(np.float32), train_y[clean_train])
        clean_scores = clean_model.predict_proba(test_matrix.astype(np.float32))[:, 1]
        full_ap = float(average_precision_score(test_y, fixed_scores))
        clean_ap = float(average_precision_score(test_y, clean_scores))

        result = diagnose_binary_endpoint(
            train_y,
            test_y,
            fixed_scores,
            test_neighbors,
            test_max,
            train_max,
            thresholds=config["profile_thresholds"],
            profile_span=tuple(config["validation_profile_span"]),
            strict_threshold=float(config["strict_threshold"]),
            high_threshold=float(config["high_similarity_threshold"]),
            clean_threshold=float(config["clean_train_threshold"]),
            min_profile_span_pp=float(config["min_profile_span_pp"]),
            min_abs_geometry=float(config["min_abs_geometry"]),
            min_test_per_class=int(config["min_test_per_class"]),
            min_clean_train_per_class=int(config["min_clean_train_per_class"]),
            min_effective_n_p10=float(config["min_effective_n_p10"]),
            hub_z_cutoff=float(config["hub_z_cutoff"]),
            hub_replicates=int(config["hub_null_replicates"]),
            seed=int(config["permutation_seed"]),
            geometry_weighting=str(config["geometry_weighting"]),
        )
        result["R_clean_retraining_pp"] = (full_ap - clean_ap) * 100.0
        endpoint = f"TAPE class {int(target_class)}"
        rows.append(
            {
                "endpoint": endpoint,
                "P_pp": result["P_profile_span_pp"],
                "A_axis": result["A_axis"],
                "hub_z": result["hub_z_max"],
                "heldout_R_pp": result["R_clean_retraining_pp"],
                "support": "Pass" if result["support_pass"] else "Fail",
                "decision": result["decision"],
                "reason": result["reason"],
            }
        )

    reference_rows = reference
    discrepancies = []
    tolerances = {"P_pp": 0.005, "A_axis": 0.005, "hub_z": 0.15, "heldout_R_pp": 0.005}
    for row in rows:
        expected = reference_rows.get(row["endpoint"])
        if expected is None:
            discrepancies.append(f"Missing released row: {row['endpoint']}")
            continue
        for field, tolerance in tolerances.items():
            ref_field = {"heldout_R_pp": "heldout_R_pp"}.get(field, field)
            if abs(float(row[field]) - float(expected[ref_field])) > tolerance:
                discrepancies.append(
                    f"{row['endpoint']} {field}: computed {row[field]:.10g}, "
                    f"released {float(expected[ref_field]):.10g} (tolerance {tolerance})"
                )
        for field in ("support", "decision"):
            if row[field] != expected[field]:
                discrepancies.append(
                    f"{row['endpoint']} {field}: computed {row[field]}, released {expected[field]}"
                )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_csv = args.output_dir / "tape_remote_validation.csv"
    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        fields = (
            "endpoint",
            "P_pp",
            "A_axis",
            "hub_z",
            "heldout_R_pp",
            "support",
            "decision",
            "reason",
        )
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    report = {
        "benchmark": "TAPE remote-homology family-holdout, one-vs-rest",
        "n_train": len(training),
        "n_test": len(test_records),
        "n_endpoints": len(rows),
        "parameters": config,
        "software_versions": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "scikit_learn": sklearn.__version__,
        },
        "numeric_comparison_tolerances": tolerances,
        "matches_released_table": not discrepancies,
        "discrepancies": discrepancies,
        "rows": rows,
    }
    (args.output_dir / "tape_remote_validation.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, indent=2))
    if discrepancies:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
