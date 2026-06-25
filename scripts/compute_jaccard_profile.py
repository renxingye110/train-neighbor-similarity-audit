from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score


def get_kmers(sequence: str, k: int = 3) -> frozenset[str]:
    if len(sequence) < k:
        return frozenset()
    return frozenset(sequence[i : i + k] for i in range(len(sequence) - k + 1))


def read_fasta(path: Path) -> list[str]:
    sequences = []
    current = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current:
                    sequences.append("".join(current))
                current = []
            else:
                current.append(line)
    if current:
        sequences.append("".join(current))
    return sequences


def compute_max_jaccard(test_sequences: list[str], train_sequences: list[str], k: int = 3) -> np.ndarray:
    len_buckets = defaultdict(list)
    train_kmers = {}
    for idx, sequence in enumerate(train_sequences):
        tokens = get_kmers(sequence, k)
        if tokens:
            train_kmers[idx] = tokens
            len_buckets[len(sequence)].append(idx)

    maxima = np.zeros(len(test_sequences), dtype=np.float32)
    for idx, sequence in enumerate(test_sequences):
        query = get_kmers(sequence, k)
        if not query:
            continue
        best = 0.0
        lo, hi = max(3, len(sequence) // 2), len(sequence) * 2
        for length in range(lo, hi + 1):
            for ref_idx in len_buckets.get(length, []):
                reference = train_kmers[ref_idx]
                overlap = len(query & reference)
                if overlap == 0:
                    continue
                score = overlap / (len(query) + len(reference) - overlap)
                if score > best:
                    best = score
                    if best >= 1.0:
                        break
            if best >= 1.0:
                break
        maxima[idx] = best
    return maxima


def evaluate_profile(predictions: np.ndarray, labels: np.ndarray, max_jaccard: np.ndarray, thresholds: list[float]) -> list[dict]:
    rows = []
    for threshold in thresholds:
        keep = max_jaccard < threshold
        kept_predictions = predictions[keep]
        kept_labels = labels[keep]
        if len(kept_predictions) >= 10 and len(np.unique(kept_labels)) == 2:
            map_value = float(average_precision_score(kept_labels, kept_predictions))
            auc_value = float(roc_auc_score(kept_labels, kept_predictions))
        else:
            map_value = None
            auc_value = None
        rows.append(
            {
                "threshold": threshold,
                "retained_n": int(keep.sum()),
                "retention_pct": round(float(keep.mean() * 100), 2),
                "mAP": None if map_value is None else round(map_value, 6),
                "AUC": None if auc_value is None else round(auc_value, 6),
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute a post hoc train-neighbor similarity profile.")
    parser.add_argument("--train_fasta", type=Path, required=True)
    parser.add_argument("--test_fasta", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--labels", type=Path, required=True)
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--thresholds", nargs="*", type=float, default=[0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00])
    args = parser.parse_args()

    train_sequences = read_fasta(args.train_fasta)
    test_sequences = read_fasta(args.test_fasta)
    predictions = np.load(args.predictions)
    labels = np.load(args.labels)
    max_jaccard = compute_max_jaccard(test_sequences, train_sequences, k=args.k)
    rows = evaluate_profile(predictions, labels, max_jaccard, args.thresholds)
    args.output.write_text(__import__("json").dumps(rows, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
