# Reproduction paths

## Main figures

Create the Python environment if you need the generic profile utility:

```bash
conda env create -f environment.yml
conda activate train-neighbor-similarity-audit
```

For the packaged figures, open MATLAB at the repository root and run:

```matlab
scripts/make_figure1
scripts/make_current_figures
```

The source tables are in `data/figure_source/`. The expected outputs are `figures/Figure_1.pdf`, `figures/Figure_2.pdf` and `figures/Figure_3.pdf`.

## Inspect the current primary screen

Open `results/primary_endpoint_release_table.csv` for all eight prespecified endpoints. The four released cases are also summarized in `data/tables/supp_table_s1_released_primary_endpoint_summary.csv`.

## Inspect supplementary checks

- `data/tables/supp_table_s2_protocol_implementation_checks.csv`
- `data/tables/supp_table_s3_primary_endpoint_screen.csv`
- `data/tables/supp_table_s4_quantitative_protocol_checks.csv`
- `data/tables/supp_table_s5_observational_equivalence_summary.csv`
- `figures/Supplementary_Figure_S1.pdf`
- `figures/Supplementary_Figure_S2.pdf`

## Compute a profile on user-supplied data

```bash
python scripts/compute_jaccard_profile.py \
  --train_fasta train.fasta \
  --test_fasta test.fasta \
  --predictions preds.npy \
  --labels labels.npy \
  --output profile.json
```

Full retraining requires the original third-party data and locally generated embeddings and is outside this compact release.
