# Reproducibility notes

This repository is meant to support review and reuse of the reported analyses. It is not a full training archive.

## Included reproduction paths

1. Reproduce the manuscript figures from the included CSV source tables using MATLAB.
2. Regenerate summary JSON files from the included machine-readable figure-source tables.
3. Compute a new post hoc train-neighbor similarity profile on user-supplied train/test FASTA files and prediction arrays with `scripts/compute_jaccard_profile.py`.

## Out of scope for this repository

- full model retraining from raw databases
- regeneration of the original local embedding matrices
- redistribution of source-database snapshots
- redistribution of checkpoint files

## File integrity

`results/checksums.tsv` records SHA256 hashes for the repository data, scripts, figures, and summary outputs.
