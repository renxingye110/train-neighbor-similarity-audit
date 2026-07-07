# Reproduction paths

This note gives the shortest practical routes through the repository, depending on what you want to check.

## 1. Reproduce the three main figures

Use the CSV files in `data/figure_source/` together with the MATLAB scripts in `scripts/`.

- Figure 1: `scripts/make_figure1.m`
- Figure 2: `scripts/make_figure2.m`
- Figure 3: `scripts/make_figure3.m`

Expected outputs are written to `figures/`.

## 2. Regenerate summary outputs

Create the Python environment first:

```bash
conda env create -f environment.yml
conda activate train-neighbor-similarity-audit
```

Then run:

```bash
python scripts/source_heldout_summary.py
python scripts/candidate_prioritization_unique.py
```

These scripts regenerate the small JSON summaries included in `results/`.

## 3. Inspect the current manuscript extension summaries

Use `results/extensions/` when you want to inspect the packaged summaries for:

- DeepLoc multitask profiles
- DeepLoc clean-retraining bridge comparisons
- broader ESCAPE multilabel and labelwise extension branches
- TAPE fluorescence and remote homology checks
- the controlled similarity-mixture simulation
- the small bridge-correlation summary across case families

These files are packaged as inspection-ready JSON summaries rather than full rerun pipelines.

## 4. Compute a similarity profile on new data

Use:

```bash
python scripts/compute_jaccard_profile.py \
  --train_fasta train.fasta \
  --test_fasta test.fasta \
  --predictions preds.npy \
  --labels labels.npy \
  --output profile.json
```

This path is generic. It is included so the post hoc performance-similarity profile can be applied to user-supplied train/test splits and prediction outputs.

## 5. Inspect manuscript tables without opening the manuscript

Use `data/tables/` for CSV exports of the manuscript and supplementary tables included in this release.

If you want the exact manuscript-to-file mapping, see `docs/manuscript_file_map.md`.
