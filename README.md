# Post hoc train-neighbor similarity auditing for biomedical protein sequence benchmarks

This repository accompanies our JBI submission on post hoc train-neighbor similarity auditing for fixed biomedical protein sequence benchmarks.

It is a compact reproducibility package rather than a full project dump. We include the processed result tables, figure source data, machine-readable manuscript tables, plotting scripts, and summary outputs needed to inspect the main results. We do not redistribute raw third-party database snapshots, large embedding arrays, checkpoint archives, or historical manuscript files.

Archived release (Zenodo DOI): https://doi.org/10.5281/zenodo.20842729

## Repository purpose

- Provide the data tables and scripts needed to reproduce the main figures without retraining models.
- Keep machine-readable versions of the manuscript tables that support the main claims.
- Document which public data sources were reused and why raw source records are not redistributed here.

This is not an AMP discovery release. The Figure 3 example is a retrospective prioritization exercise that shows how a similarity constraint can change a fixed candidate ranking.

## Start here

If you only need a quick orientation, use these three documents:

- `docs/repository_guide.md`: what each top-level folder is for
- `docs/reproduction_paths.md`: the shortest route to reproduce figures or summaries
- `docs/manuscript_file_map.md`: where each figure and manuscript table lives in the repository

## Quick start

### Python environment

```bash
conda env create -f environment.yml
conda activate train-neighbor-similarity-audit
python scripts/source_heldout_summary.py
python scripts/candidate_prioritization_unique.py
```

### Reproduce the manuscript figures

The main figures were rendered in MATLAB from the CSV files in `data/figure_source/`.

```text
Open scripts/make_figure1.m in MATLAB and run it.
Open scripts/make_figure2.m in MATLAB and run it.
Open scripts/make_figure3.m in MATLAB and run it.
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
- MATLAB: scripts were last harmonized for the v191 JBI artwork pass

Reproducing the figures from the included tables should take only a few minutes once the environment is set up. Full model retraining is outside the scope of this repository.

## Repository layout

- `data/figure_source/`: source tables for Figures 1-3
- `data/tables/`: machine-readable CSV exports from the current main manuscript and supplement
- `scripts/`: a generic Jaccard-profile CLI, summary scripts for the source-held-out and retrospective prioritization analyses, and MATLAB figure scripts
- `results/`: summary JSON exports and file checksums
- `figures/`: final exported figures and graphical abstract PDF

More detail is provided in `docs/repository_guide.md`.

## What is not redistributed

- raw third-party peptide or protein sequence database dumps
- large local embedding arrays
- model checkpoints
- historical manuscript versions
- internal planning files, prompt logs, or agent notes

Raw third-party records should be obtained from the original cited sources listed in `docs/third_party_data_sources.md`.

## Manuscript file map

The figure-to-file and table-to-file mapping is collected in `docs/manuscript_file_map.md`.

## License and reuse

- Code in this repository is released under the MIT License.
- Derived result tables remain subject to the license and reuse conditions of the original source databases when those conditions apply.
- This repository does not grant rights to redistribute third-party raw database records.

## Data and code availability text

Suggested manuscript text is provided in `docs/data_code_availability_statement.md`.
