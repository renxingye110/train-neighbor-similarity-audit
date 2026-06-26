# Repository guide

This repository is organized as a compact reproducibility package. The goal is to make the reported figures, summary tables, and supporting scripts easy to inspect without requiring the full local project history.

## Top-level folders

- `data/figure_source/`
  Source tables used to build Figures 1-3.

- `data/tables/`
  Machine-readable CSV exports of the manuscript and supplementary tables included in this release.

- `scripts/`
  MATLAB figure scripts and lightweight Python utilities used for summary generation and generic profile computation.

- `results/`
  Small JSON summaries and file checksums for the packaged outputs.

- `figures/`
  Final exported main figures and the graphical abstract PDF.

- `docs/`
  Short companion notes for repository use, data provenance, and manuscript statements.

## What this repository is meant for

- Reproducing the reported main figures from packaged source tables
- Inspecting machine-readable versions of the manuscript tables
- Reviewing the source-held-out summary outputs
- Reviewing the retrospective Figure 3 prioritization example
- Running the generic k-mer Jaccard profile script on new user-supplied inputs

## What this repository is not meant for

- Full retraining from raw source databases
- Regeneration of local embedding matrices
- Redistribution of raw third-party sequence database snapshots
- Distribution of model checkpoints or other local working files

## First places to look

- Start with `README.md` for the shortest overview
- Use `docs/reproduction_paths.md` for figure or summary reproduction
- Use `docs/manuscript_file_map.md` if you want to match manuscript items to repository files
