from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from benchmark_diagnostic import (  # noqa: E402
    build_kmer_matrix,
    class_conditional_hub_z,
    map_kmer_matrix,
    profile_metrics,
    top_neighbors,
    unique_kmers,
    weighted_geometry,
)


class SimilarityProfileTests(unittest.TestCase):
    def test_unique_kmers_discards_repeated_tokens(self) -> None:
        self.assertEqual(unique_kmers("AAAAA", 3), frozenset({"AAA"}))

    def test_top_neighbor_uses_jaccard_and_length_window(self) -> None:
        reference, ref_len, ref_count, vocab = build_kmer_matrix(
            ["AACCGG", "TTTTTT"], k=3
        )
        query, query_len, query_count = map_kmer_matrix(["AACCGG"], vocab, k=3)
        neighbors, maxima = top_neighbors(
            query, query_len, query_count, reference, ref_len, ref_count, top_k=2
        )
        self.assertEqual(neighbors[0][0][0], 0)
        self.assertEqual(neighbors[0][0][1], 1.0)
        self.assertEqual(maxima.tolist(), [1.0])

    def test_profile_threshold_is_strict(self) -> None:
        rows = profile_metrics(
            np.asarray([1, 0, 1, 0]),
            np.asarray([0.9, 0.8, 0.2, 0.1]),
            np.asarray([0.2, 0.4, 0.6, 1.0]),
            thresholds=[0.5, 0.7],
            min_samples=1,
        )
        self.assertEqual(rows[0]["retained_n"], 2)
        self.assertEqual(rows[1]["retained_n"], 3)

    def test_weighted_geometry_is_chance_corrected(self) -> None:
        result = weighted_geometry(
            neighbors=[[(0, 0.8), (1, 0.2)]],
            train_labels=np.asarray([0, 1]),
            test_labels=np.asarray([0]),
        )
        self.assertAlmostEqual(result["agreement"][0], 0.8)
        self.assertAlmostEqual(result["chance_corrected"][0], 0.6)
        self.assertAlmostEqual(result["n_eff"][0], 1.0 / (0.8**2 + 0.2**2))

    def test_hub_null_is_reproducible(self) -> None:
        neighbors = [[(0, 0.8), (1, 0.6)], [(0, 0.7), (2, 0.5)]]
        labels = np.asarray([0, 1])
        first = class_conditional_hub_z(
            neighbors, labels, 10, np.random.default_rng(19), replicates=50
        )
        second = class_conditional_hub_z(
            neighbors, labels, 10, np.random.default_rng(19), replicates=50
        )
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
