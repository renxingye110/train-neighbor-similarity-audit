from __future__ import annotations

import argparse
import csv
import json
import platform
import sys
from pathlib import Path
from typing import Any

import numpy as np
import scipy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from benchmark_diagnostic import (  # noqa: E402
    build_kmer_matrix,
    diagnose_binary_endpoint,
    map_kmer_matrix,
    top_neighbors,
)


def read_records(path: Path, required: tuple[str, ...]) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = set(required) - set(reader.fieldnames or ())
        if missing:
            raise ValueError(f"{path} is missing columns: {sorted(missing)}")
        return list(reader)


def finite_json(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: finite_json(item) for key, item in value.items()}
    if isinstance(value, list):
        return [finite_json(item) for item in value]
    if isinstance(value, (np.floating, float)):
        return float(value) if np.isfinite(value) else None
    if isinstance(value, np.integer):
        return int(value)
    return value


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the P/A/S diagnostic on a fixed binary-classifier output."
    )
    parser.add_argument("--train", type=Path, required=True, help="CSV: sequence,label")
    parser.add_argument(
        "--test", type=Path, required=True, help="CSV: sequence,label,score"
    )
    parser.add_argument(
        "--output-dir", type=Path, required=True, help="Directory for profile and JSON outputs"
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=ROOT / "configs" / "released_analysis.json",
    )
    parser.add_argument(
        "--profile-span",
        nargs=2,
        type=float,
        default=None,
        metavar=("LOW", "HIGH"),
        help="Threshold pair for P; defaults to the validation pair in the config.",
    )
    parser.add_argument(
        "--geometry-weighting",
        choices=("sample", "class_balanced"),
        default=None,
        help="Average A across samples or average class-specific means equally.",
    )
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    train_rows = read_records(args.train, ("sequence", "label"))
    test_rows = read_records(args.test, ("sequence", "label", "score"))
    if not train_rows or not test_rows:
        raise ValueError("Training and test CSV files must contain records")

    train_sequences = [row["sequence"].strip().upper() for row in train_rows]
    test_sequences = [row["sequence"].strip().upper() for row in test_rows]
    train_labels = np.asarray([int(row["label"]) for row in train_rows], dtype=np.int8)
    test_labels = np.asarray([int(row["label"]) for row in test_rows], dtype=np.int8)
    scores = np.asarray([float(row["score"]) for row in test_rows], dtype=np.float64)
    if not np.isfinite(scores).all() or ((scores < 0) | (scores > 1)).any():
        raise ValueError("score values must be finite probabilities in [0, 1]")

    train_matrix, train_lengths, train_counts, token_to_column = build_kmer_matrix(
        train_sequences, int(config["kmer_size"])
    )
    test_matrix, test_lengths, test_counts = map_kmer_matrix(
        test_sequences, token_to_column, int(config["kmer_size"])
    )
    neighbors, test_max = top_neighbors(
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

    profile_span = tuple(args.profile_span or config["validation_profile_span"])
    result = diagnose_binary_endpoint(
        train_labels,
        test_labels,
        scores,
        neighbors,
        test_max,
        train_max,
        thresholds=config["profile_thresholds"],
        profile_span=profile_span,
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
        geometry_weighting=str(args.geometry_weighting or config["geometry_weighting"]),
    )
    output = {
        "metadata": {
            "n_train": len(train_rows),
            "n_test": len(test_rows),
            "kmer_size": int(config["kmer_size"]),
            "top_k": int(config["top_k"]),
            "profile_span": list(profile_span),
            "metric": "average precision",
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "diagnostic": result,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "diagnostic.json").write_text(
        json.dumps(finite_json(output), indent=2), encoding="utf-8"
    )
    with (args.output_dir / "profile.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        fields = ("threshold", "retained_n", "retention_pct", "average_precision")
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(result["profile"])
    print(json.dumps(finite_json(output["diagnostic"]), indent=2))


if __name__ == "__main__":
    main()
