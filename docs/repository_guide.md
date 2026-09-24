# Repository guide

This repository is the compact reproducibility package for the current manuscript, **Similarity-stratified retraining sensitivity in fixed protein-sequence benchmarks**.

## Top-level folders

- `data/figure_source/`: source CSV files for the current main and supplementary figures.
- `data/tables/`: machine-readable Table 1 and Supplementary Tables S1-S6.
- `scripts/`: the generic Jaccard-profile CLI, the Figure 1 script and the current Figure 2/3 script.
- `results/`: the complete eight-endpoint primary screen, release summary and screened-outcome archive.
- `figures/`: exported current main and supplementary figures.
- `docs/`: manuscript mapping, reproduction paths, data availability and provenance notes.

## Current evidence package

The current release is organized around:

1. the ESCAPE antibacterial train-fold-only PCA development endpoint;
2. the ESCAPE antifungal within-benchmark confirmation;
3. the exhaustive seven-label TAPE remote-homology external validation screen;
4. the four released cases and four abstained cases in the complete endpoint table;
5. the train-only PCA, complete-pool PCA sensitivity, three-seed, bootstrap and similarity-proxy checks;
6. the observational-equivalence stress-test summary.

The repository includes processed outputs and source data for inspection and figure reproduction. It does not redistribute raw third-party sequence snapshots, embedding caches, model checkpoints or failed-submission historical artifacts.
