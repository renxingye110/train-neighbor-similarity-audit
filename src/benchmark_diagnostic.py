"""Core similarity-profile, label-geometry, and support-gate calculations."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

import numpy as np
from scipy.sparse import csr_matrix
from sklearn.metrics import average_precision_score


DEFAULT_THRESHOLDS = (0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00)


def unique_kmers(sequence: str, k: int = 3) -> frozenset[str]:
    if k < 1:
        raise ValueError("k must be positive")
    if len(sequence) < k:
        return frozenset()
    return frozenset(sequence[i : i + k] for i in range(len(sequence) - k + 1))


def build_kmer_matrix(
    sequences: list[str], k: int = 3
) -> tuple[csr_matrix, np.ndarray, np.ndarray, dict[str, int]]:
    token_to_column: dict[str, int] = {}
    row_indices: list[int] = []
    column_indices: list[int] = []
    counts = np.zeros(len(sequences), dtype=np.int32)
    lengths = np.asarray([len(sequence) for sequence in sequences], dtype=np.int32)

    for row, sequence in enumerate(sequences):
        tokens = sorted(unique_kmers(sequence, k))
        counts[row] = len(tokens)
        for token in tokens:
            column = token_to_column.setdefault(token, len(token_to_column))
            row_indices.append(row)
            column_indices.append(column)

    values = np.ones(len(row_indices), dtype=np.uint8)
    matrix = csr_matrix(
        (values, (row_indices, column_indices)),
        shape=(len(sequences), len(token_to_column)),
        dtype=np.uint8,
    )
    return matrix, lengths, counts, token_to_column


def map_kmer_matrix(
    sequences: list[str], token_to_column: dict[str, int], k: int = 3
) -> tuple[csr_matrix, np.ndarray, np.ndarray]:
    row_indices: list[int] = []
    column_indices: list[int] = []
    counts = np.zeros(len(sequences), dtype=np.int32)
    lengths = np.asarray([len(sequence) for sequence in sequences], dtype=np.int32)

    for row, sequence in enumerate(sequences):
        columns = [
            token_to_column[token]
            for token in unique_kmers(sequence, k)
            if token in token_to_column
        ]
        counts[row] = len(columns)
        row_indices.extend([row] * len(columns))
        column_indices.extend(columns)

    values = np.ones(len(row_indices), dtype=np.uint8)
    matrix = csr_matrix(
        (values, (row_indices, column_indices)),
        shape=(len(sequences), len(token_to_column)),
        dtype=np.uint8,
    )
    return matrix, lengths, counts


def top_neighbors(
    query_matrix: csr_matrix,
    query_lengths: np.ndarray,
    query_counts: np.ndarray,
    reference_matrix: csr_matrix,
    reference_lengths: np.ndarray,
    reference_counts: np.ndarray,
    top_k: int = 20,
    batch_size: int = 64,
    k: int = 3,
) -> tuple[list[list[tuple[int, float]]], np.ndarray]:
    if top_k < 1:
        raise ValueError("top_k must be positive")
    reference_t = reference_matrix.transpose().tocsr()
    neighbors: list[list[tuple[int, float]]] = [[] for _ in range(query_matrix.shape[0])]
    maxima = np.zeros(query_matrix.shape[0], dtype=np.float64)

    for start in range(0, query_matrix.shape[0], batch_size):
        stop = min(start + batch_size, query_matrix.shape[0])
        products = (query_matrix[start:stop] @ reference_t).tocsr()
        for local_row in range(products.shape[0]):
            query_index = start + local_row
            row = products.getrow(local_row)
            if row.nnz == 0:
                continue

            candidates = row.indices
            intersections = row.data.astype(np.float64)
            query_length = int(query_lengths[query_index])
            lo = max(k, query_length // 2)
            hi = query_length * 2
            length_ok = (reference_lengths[candidates] >= lo) & (
                reference_lengths[candidates] <= hi
            )
            candidates = candidates[length_ok]
            intersections = intersections[length_ok]
            if len(candidates) == 0:
                continue

            unions = query_counts[query_index] + reference_counts[candidates] - intersections
            similarities = intersections / unions
            # Resolve equal similarities by training-row order for repeatable top-k edges.
            order = np.lexsort((candidates, -similarities))[:top_k]
            pairs = [
                (int(candidates[position]), float(similarities[position]))
                for position in order
            ]
            neighbors[query_index] = pairs
            maxima[query_index] = pairs[0][1]

    return neighbors, maxima


def weighted_geometry(
    neighbors: list[list[tuple[int, float]]],
    train_labels: np.ndarray,
    test_labels: np.ndarray,
) -> dict[str, np.ndarray]:
    classes, class_counts = np.unique(train_labels, return_counts=True)
    prevalence = {
        label: count / len(train_labels) for label, count in zip(classes, class_counts)
    }
    agreement = np.full(len(test_labels), np.nan, dtype=np.float64)
    corrected = np.full(len(test_labels), np.nan, dtype=np.float64)
    effective_n = np.zeros(len(test_labels), dtype=np.float64)

    for index, pairs in enumerate(neighbors):
        if not pairs:
            continue
        train_indices = np.asarray([pair[0] for pair in pairs], dtype=np.int64)
        weights = np.asarray([pair[1] for pair in pairs], dtype=np.float64)
        total_weight = float(weights.sum())
        if total_weight <= 0:
            continue

        same_label = (train_labels[train_indices] == test_labels[index]).astype(np.float64)
        agreement[index] = float(np.average(same_label, weights=weights))
        expected = float(prevalence.get(test_labels[index], 0.0))
        if expected < 1.0:
            corrected[index] = (agreement[index] - expected) / (1.0 - expected)
        effective_n[index] = total_weight**2 / float(np.square(weights).sum())

    return {"agreement": agreement, "chance_corrected": corrected, "n_eff": effective_n}


def class_conditional_hub_z(
    neighbors: list[list[tuple[int, float]]],
    test_labels: np.ndarray,
    n_train: int,
    rng: np.random.Generator,
    replicates: int = 1000,
) -> dict[str, Any]:
    train_edges: list[int] = []
    test_edges: list[int] = []
    for query_index, pairs in enumerate(neighbors):
        for train_index, _ in pairs:
            train_edges.append(train_index)
            test_edges.append(query_index)

    train_edges_array = np.asarray(train_edges, dtype=np.int64)
    test_edges_array = np.asarray(test_edges, dtype=np.int64)
    classes = np.unique(test_labels)
    top_n = max(1, int(np.ceil(0.01 * n_train)))

    def top_shares(assigned_labels: np.ndarray) -> np.ndarray:
        shares = []
        for label in classes:
            selected = train_edges_array[
                assigned_labels[test_edges_array] == label
            ]
            counts = np.bincount(selected, minlength=n_train).astype(np.float64)
            shares.append(
                float(np.sort(counts)[-top_n:].sum() / counts.sum())
                if counts.sum()
                else 0.0
            )
        return np.asarray(shares, dtype=np.float64)

    observed = top_shares(test_labels)
    null = np.asarray(
        [top_shares(rng.permutation(test_labels)) for _ in range(replicates)],
        dtype=np.float64,
    )
    null_mean = null.mean(axis=0)
    null_sd = null.std(axis=0, ddof=1) if replicates > 1 else np.zeros(len(classes))
    z_values = np.divide(
        observed - null_mean,
        null_sd,
        out=np.zeros_like(observed),
        where=null_sd > 0,
    )
    return {
        "classes": classes.tolist(),
        "observed_top1_share": observed.tolist(),
        "null_mean": null_mean.tolist(),
        "null_sd": null_sd.tolist(),
        "z_by_class": z_values.tolist(),
        "hub_z_max": float(np.max(z_values)) if len(z_values) else 0.0,
    }


def profile_metrics(
    labels: np.ndarray,
    scores: np.ndarray,
    max_similarity: np.ndarray,
    thresholds: tuple[float, ...] | list[float] = DEFAULT_THRESHOLDS,
    min_samples: int = 30,
) -> list[dict[str, Any]]:
    rows = []
    for threshold in thresholds:
        keep = max_similarity < threshold
        y = labels[keep]
        value = None
        if keep.sum() >= min_samples and len(np.unique(y)) == 2:
            value = float(average_precision_score(y, scores[keep]))
        rows.append(
            {
                "threshold": float(threshold),
                "retained_n": int(keep.sum()),
                "retention_pct": float(keep.mean() * 100.0) if len(keep) else 0.0,
                "average_precision": value,
            }
        )
    return rows


def diagnose_binary_endpoint(
    train_labels: np.ndarray,
    test_labels: np.ndarray,
    fixed_scores: np.ndarray,
    neighbors: list[list[tuple[int, float]]],
    test_max_similarity: np.ndarray,
    train_max_similarity: np.ndarray,
    *,
    thresholds: tuple[float, ...] | list[float] = DEFAULT_THRESHOLDS,
    profile_span: tuple[float, float] = (0.40, 1.00),
    strict_threshold: float = 0.40,
    high_threshold: float = 0.60,
    clean_threshold: float = 0.40,
    min_profile_span_pp: float = 5.0,
    min_abs_geometry: float = 0.10,
    min_test_per_class: int = 25,
    min_clean_train_per_class: int = 25,
    min_effective_n_p10: float = 5.0,
    hub_z_cutoff: float = 23.704131673352453,
    hub_replicates: int = 1000,
    seed: int = 20260922,
    geometry_weighting: str = "sample",
) -> dict[str, Any]:
    if len(test_labels) != len(fixed_scores) or len(test_labels) != len(test_max_similarity):
        raise ValueError("test labels, scores, and test similarities must have equal length")
    if len(train_labels) != len(train_max_similarity):
        raise ValueError("training labels and training similarities must have equal length")
    if not np.isin(train_labels, (0, 1)).all() or not np.isin(test_labels, (0, 1)).all():
        raise ValueError("This entry point expects binary labels encoded as 0 and 1")
    if geometry_weighting not in {"sample", "class_balanced"}:
        raise ValueError("geometry_weighting must be 'sample' or 'class_balanced'")

    profile = profile_metrics(test_labels, fixed_scores, test_max_similarity, thresholds)
    profile_by_threshold = {row["threshold"]: row["average_precision"] for row in profile}
    low, high = map(float, profile_span)
    p_value = None
    if profile_by_threshold.get(low) is not None and profile_by_threshold.get(high) is not None:
        p_value = (profile_by_threshold[high] - profile_by_threshold[low]) * 100.0

    geometry = weighted_geometry(neighbors, train_labels, test_labels)
    corrected = geometry["chance_corrected"]
    strict = test_max_similarity < strict_threshold
    high_similarity = test_max_similarity >= high_threshold

    def group_mean(mask: np.ndarray) -> float:
        valid = mask & np.isfinite(corrected)
        if not valid.any():
            return float("nan")
        if geometry_weighting == "sample":
            return float(corrected[valid].mean())
        class_means = [
            float(corrected[valid & (test_labels == label)].mean())
            for label in np.unique(test_labels[valid])
        ]
        return float(np.mean(class_means))

    strict_geometry = group_mean(strict)
    high_geometry = group_mean(high_similarity)
    a_value = high_geometry - strict_geometry
    clean_train = train_max_similarity < clean_threshold
    strict_counts = {
        str(label): int(np.sum(strict & (test_labels == label))) for label in (0, 1)
    }
    clean_counts = {
        str(label): int(np.sum(clean_train & (train_labels == label)))
        for label in (0, 1)
    }
    strict_neff = geometry["n_eff"][strict & np.isfinite(geometry["n_eff"])]
    neff_p10 = float(np.quantile(strict_neff, 0.10)) if len(strict_neff) else float("nan")
    hub = class_conditional_hub_z(
        neighbors,
        test_labels,
        len(train_labels),
        np.random.default_rng(seed),
        hub_replicates,
    )

    support_reason = "pass"
    if min(strict_counts.values()) < min_test_per_class:
        support_reason = "strict-class-support failure"
    elif min(clean_counts.values()) < min_clean_train_per_class:
        support_reason = "clean-train-class-support failure"
    elif not np.isfinite(neff_p10) or neff_p10 < min_effective_n_p10:
        support_reason = "effective-support failure"
    elif hub["hub_z_max"] > hub_z_cutoff:
        support_reason = "hub-concentration failure"

    pa_aligned = bool(
        p_value is not None
        and np.isfinite(a_value)
        and abs(p_value) >= min_profile_span_pp
        and abs(a_value) >= min_abs_geometry
        and np.sign(p_value) == np.sign(a_value)
    )
    support_pass = support_reason == "pass"
    released = bool(pa_aligned and support_pass)
    if released:
        decision_reason = "Primary released case"
    elif not support_pass:
        decision_reason = {
            "strict-class-support failure": "Strict class support",
            "clean-train-class-support failure": "Clean class support",
            "effective-support failure": "Effective neighbor support",
            "hub-concentration failure": "Hub-z concentration",
        }[support_reason]
    else:
        decision_reason = "Low profile/geometry signal"

    return {
        "P_profile_span_pp": p_value,
        "A_axis": float(a_value),
        "hub_z_max": float(hub["hub_z_max"]),
        "support_pass": support_pass,
        "support_reason": support_reason,
        "strict_n": int(strict.sum()),
        "strict_class_counts": strict_counts,
        "clean_train_class_counts": clean_counts,
        "strict_neff_p10": neff_p10,
        "P_plus_A": pa_aligned,
        "P_plus_A_plus_S": released,
        "decision": "Released" if released else "Abstained",
        "reason": decision_reason,
        "profile": profile,
        "support": hub,
    }
