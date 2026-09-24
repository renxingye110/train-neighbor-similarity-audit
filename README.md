# Reproducibility package for similarity-stratified retraining sensitivity in fixed protein-sequence benchmarks

This repository accompanies the manuscript "Similarity-stratified retraining sensitivity in fixed protein-sequence benchmarks."

This repository is a compact reproducibility package rather than a full project dump. It includes the processed result tables, figure source data, machine-readable manuscript tables, plotting scripts, and summary outputs needed to inspect the reported results. It does not redistribute raw third-party database snapshots, large embedding arrays, checkpoint archives, historical manuscript files, or submission-only artwork assets.

Current Zenodo concept DOI (latest version): https://doi.org/10.5281/zenodo.20842728

## Repository purpose

- Provide the data tables and scripts needed to reproduce the main figures without retraining models.
- Keep machine-readable versions of the manuscript tables that support the main claims.
- Package the complete eight-endpoint primary screen, released-case summaries, protocol checks and supporting source data discussed in the current manuscript and Supplementary Tables S1-S5.
- Document which public data sources were reused and why raw source records are not redistributed here.

This is not an AMP discovery release. The primary validation compares a fixed ESCAPE antifungal endpoint with an exhaustive seven-label TAPE remote-homology family-holdout screen. Four of eight prespecified endpoints satisfy the release rule; the complete endpoint denominator is retained in the machine-readable tables.

## Citation

If you use this repository, please cite the Zenodo record:

Ren X. Reproducibility materials for similarity-stratified retraining sensitivity in fixed protein-sequence benchmarks. Zenodo. 2026. doi: 10.5281/zenodo.20842728

## Start here

If you only need a quick orientation, use these three documents:

- `docs/repository_guide.md`: what each top-level folder is for
- `docs/reproduction_paths.md`: the shortest route to reproduce figures or summaries
- `docs/manuscript_file_map.md`: where each figure and manuscript table lives in the repository
- `docs/current_manuscript_extensions.md`: current primary screen, protocol checks and repository scope

## Quick start

### Python environment

```bash
conda env create -f environment.yml
conda activate train-neighbor-similarity-audit
python scripts/compute_jaccard_profile.py --help
```

### Reproduce the manuscript figures

The main figures were rendered in MATLAB from the CSV files in `data/figure_source/`.

```text
Open scripts/make_figure1.m in MATLAB and run it.
Open scripts/make_current_figures.m in MATLAB and run it.
```

Expected outputs:

- `figures/Figure_1.pdf`
- `figures/Figure_2.pdf`
- `figures/Figure_3.pdf`

### Generic similarity-profile computation on new data

```bash
python scripts/compute_jaccard_profile.py \
  --train_fasta train.fasta \
  --test_fasta test.fasta \
  --predictions preds.npy \
  --labels labels.npy \
  --output profile.json
```

## Software versions

- Python: 3.10
- NumPy / pandas / scikit-learn: see `environment.yml`
- MATLAB: see the figure scripts for the plotting and export settings used for the packaged figures

Reproducing the figures from the included tables should take only a few minutes once the environment is set up. Full model retraining is outside the scope of this repository.

## Repository layout

- `data/figure_source/`: source tables for Figures 1-3
- `data/tables/`: machine-readable CSV exports of the manuscript and supplementary tables included in this release
- `scripts/`: the generic Jaccard-profile CLI and current MATLAB figure script
- `results/`: primary endpoint summaries, screened-outcome archive and file checksums
- `figures/`: final exported main and supplementary figures

More detail is provided in `docs/repository_guide.md`.

## What is not redistributed

- raw third-party peptide or protein sequence database dumps
- large local embedding arrays
- model checkpoints
- historical manuscript versions
- private planning notes or other local working materials

Raw third-party records should be obtained from the original cited sources listed in `docs/third_party_data_sources.md`.

Earlier manuscript versions are not included in the current release.

## Manuscript file map

The figure-to-file and table-to-file mapping is collected in `docs/manuscript_file_map.md`.

## License and reuse

- Code in this repository is released under the MIT License.
- Derived result tables remain subject to the license and reuse conditions of the original source databases when those conditions apply.
- This repository does not grant rights to redistribute third-party raw database records.

## Data and code availability text

Suggested manuscript text is provided in `docs/data_code_availability_statement.md`.
