# Post hoc train-neighbor similarity auditing for biomedical protein sequence benchmarks

This repository accompanies our JBI submission on post hoc train-neighbor similarity auditing for fixed biomedical protein sequence benchmarks.

It is a compact reproducibility package rather than a full project dump. We include the processed result tables, figure source data, machine-readable manuscript tables, plotting scripts, and summary outputs needed to inspect the main results. We do not redistribute raw third-party database snapshots, large embedding arrays, checkpoint archives, or historical manuscript files.

## Repository purpose

- Provide the data tables and scripts needed to reproduce the main figures without retraining models.
- Keep machine-readable versions of the manuscript tables that support the main claims.
- Document which public data sources were reused and why raw source records are not redistributed here.

This is not an AMP discovery release. The Figure 3 example is a retrospective prioritization exercise that shows how a similarity constraint can change a fixed candidate ranking.

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

## What is included

- `data/figure_source/`: source tables for Figures 1-3
- `data/tables/`: machine-readable CSV exports from the current main manuscript and supplement
- `scripts/`: a generic Jaccard-profile CLI, summary scripts for the source-held-out and retrospective prioritization analyses, and MATLAB figure scripts
- `results/`: summary JSON exports and file checksums
- `figures/`: final exported figures and graphical abstract PDF

## What is not redistributed

- raw third-party peptide or protein sequence database dumps
- large local embedding arrays
- model checkpoints
- historical manuscript versions
- internal planning files, prompt logs, or agent notes

Raw third-party records should be obtained from the original cited sources listed in `docs/third_party_data_sources.md`.

## Mapping from manuscript items to repository files

### Main figures

- Figure 1 -> `data/figure_source/figure1_threshold_profile.csv`, `data/figure_source/figure1_auc_profile.csv`, `scripts/make_figure1.m`
- Figure 2 -> `data/figure_source/figure2_source_heldout_profiles.csv`, `data/figure_source/figure2_endpoint_spans.csv`, `data/figure_source/figure2_retraining_changes.csv`, `scripts/make_figure2.m`
- Figure 3 -> `data/figure_source/figure3_unique_candidate_pool_summary.csv`, `data/figure_source/figure3_candidate_pool_points.csv`, `data/figure_source/figure3_raw_top20.csv`, `data/figure_source/figure3_audited_top20.csv`, `data/figure_source/figure3_similarity_composition.csv`, `scripts/make_figure3.m`

### Main manuscript tables

- Table 1 -> `data/tables/table1_data_flow.csv`
- Table 2 -> `data/tables/table2_ablation_clean_retraining.csv`
- Table 3 -> `data/tables/table3_threshold_retained_subset.csv`
- Table 4 -> `data/tables/table4_prevalence_matched_ap.csv`

### Supplementary tables

- Supplementary Table S1 -> `data/tables/supp_table_s1_length_strata.csv`
- Supplementary Table S2 -> `data/tables/supp_table_s2_runtime_by_configuration.csv`
- Supplementary Table S3 -> `data/tables/supp_table_s3_clean_fold_sizes.csv`
- Supplementary Table S4 -> `data/tables/supp_table_s4_multik_sensitivity.csv`
- Supplementary Table S5 -> `data/tables/supp_table_s5_method_comparison.csv`
- Supplementary Table S6 -> `data/tables/supp_table_s6_hemolysis_label_audit_categories.csv`
- Supplementary Table S7 -> `data/tables/supp_table_s7_ll37_truncation_primary_hcs.csv`
- Supplementary Table S7b -> `data/tables/supp_table_s7b_ll37_bucketed_vs_unbucketed_hcs.csv`
- Supplementary Table S8 -> `data/tables/supp_table_s8_ampcliff_hcs_summary.csv`
- Supplementary Table S9 -> `data/tables/supp_table_s9_cross_plm_curve_spans.csv`
- Supplementary Table S10 -> `data/tables/supp_table_s10_cross_plm_threshold_data.csv`
- Supplementary Table S11 -> `data/tables/supp_table_s11_source_heldout_summary.csv`
- Supplementary Table S12 -> `data/tables/supp_table_s12_source_heldout_threshold_data.csv`
- Supplementary Table S13 -> `data/tables/supp_table_s13_source_heldout_per_seed.csv`
- Supplementary Table S14 -> `data/tables/supp_table_s14_grl_lambda_sweep.csv`
- Supplementary Table S15 -> `data/tables/supp_table_s15_hcse_alpha_sweep.csv`
- Supplementary Table S16 -> `data/tables/supp_table_s16_hcse_threshold_data.csv`
- Supplementary Table S17 -> `data/tables/supp_table_s17_candidate_pool_summary.csv`
- Supplementary Table S18 -> `data/tables/supp_table_s18_candidate_top20_summary.csv`
- Supplementary Table S19 -> `data/tables/supp_table_s19_changed_candidates.csv`

## License and reuse

- Code in this repository is released under the MIT License.
- Derived result tables remain subject to the license and reuse conditions of the original source databases when those conditions apply.
- This repository does not grant rights to redistribute third-party raw database records.

## Data and code availability text

Suggested manuscript text is provided in `docs/data_code_availability_statement.md`.
