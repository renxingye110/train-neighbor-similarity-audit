# Post hoc train-neighbor similarity auditing for biomedical protein sequence benchmarks

This repository contains the current JBI submission-facing reproducibility package for a post hoc train-neighbor similarity audit of fixed biomedical protein sequence benchmarks.

The package is intentionally small. It does not redistribute raw third-party database dumps, large embedding matrices, checkpoint archives, or historical manuscript files. Instead, it provides the processed result tables, figure source data, machine-readable manuscript tables, plotting scripts, and summary outputs needed to inspect and reproduce the reported main figures and selected supplementary analyses.

## Repository purpose

- Support a post hoc train-neighbor similarity audit for fixed biomedical protein sequence benchmarks.
- Reproduce the main manuscript figures from source tables without retraining.
- Preserve machine-readable versions of the tables that support the main claims.
- Document which source databases were reused and why the raw third-party records are not redistributed here.

This repository is not an AMP discovery release. The Figure 3 example is a retrospective prioritization analysis used to illustrate how a similarity constraint changes a fixed candidate ranking.

## Quick start

### Python environment

```bash
conda env create -f environment.yml
conda activate train-neighbor-similarity-audit
python scripts/source_heldout_summary.py
python scripts/candidate_prioritization_unique.py
```

### Reproduce the manuscript figures

Main figures were rendered with MATLAB from the CSV files in `data/figure_source/`.

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

The figure-table reproduction path is lightweight and should run within minutes once the environment is available. Full model retraining is intentionally out of scope for this minimal repository.

## What is included

- `data/figure_source/`: source tables for Figures 1-3
- `data/tables/`: machine-readable CSV exports from the current main manuscript and supplement
- `scripts/`: a generic Jaccard-profile CLI, summary scripts for the source-held-out and retrospective prioritization analyses, and MATLAB figure scripts
- `results/`: summary JSON exports and file checksums
- `figures/`: current final exported figures and graphical abstract PDF

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

- Table 1. Data flow from source records to the evaluation subset. Counts distinguish the local preprocessing scope from the fixed ESCAPE fold-mapped subset used for model evaluation. -> `data/tables/table1_data_flow.csv`
- Table 2. Two-by-two factor ablation with de novo Jaccard-0.40 clean-fold retraining. Clean mAP refers to models retrained on Jaccard-0.40 clean folds, not to the retained subsets in Table 3. -> `data/tables/table2_ablation_clean_retraining.csv`
- Table 3. Multi-threshold k-mer Jaccard retained-subset analysis for the ESM-2 classifier and the k-mer logistic-regression baseline. -> `data/tables/table3_threshold_retained_subset.csv`
- Table 4. Prevalence-controlled average-precision sensitivity check. Each threshold was resampled to the class counts of the 0.30 retained subset before average precision was recalculated. -> `data/tables/table4_prevalence_matched_ap.csv`

### Supplementary tables

- Supplementary Table S1. Length-stratified multi-threshold k-mer Jaccard performance-similarity curve. -> `data/tables/supp_table_s1_length_strata.csv`
- Supplementary Table S2. Training and evaluation runtime by configuration. -> `data/tables/supp_table_s2_runtime_by_configuration.csv`
- Supplementary Table S3. Fold sample counts and Jaccard-0.40 retention rates. -> `data/tables/supp_table_s3_clean_fold_sizes.csv`
- Supplementary Table S4. Multi-k sensitivity analysis for the k-mer Jaccard performance-similarity curve. -> `data/tables/supp_table_s4_multik_sensitivity.csv`
- Supplementary Table S5. Comparison of similarity-aware evaluation methods. -> `data/tables/supp_table_s5_method_comparison.csv`
- During database quality control, we systematically audited hemolytic-activity labels across 13 databases and found a semantic parsing error. In DRAMP [26], 5,563 sequence records contained the hemolytic_activity value "No hemolysis information or data found in the reference(s) presented in this entry". This text clearly indicates that experimental hemolysis testing was not available. A substring-matching classifier triggered by the shared prefix "no hemolys" confused all 5,563 untested records with eight records whose field value was "No hemolysis", which denotes experimentally verified non-hemolysis. This produced a misclassification ratio of 695:1. -> `data/tables/supp_table_s6_hemolysis_label_audit_categories.csv`
- We applied HCS diagnostics to three experimentally active truncation variants of human cathelicidin LL-37, using configuration G (ampmodel_single_1280d) and length-bucketed k-mer Jaccard. Source: Pennone et al. [48]. Jmax denotes maximum 3-mer Jaccard to the ESCAPE training set. h_t denotes the Jaccard-weighted mean prediction of similar training sequences. r_t denotes prediction minus h_t. HCS% is h_t divided by prediction, multiplied by 100. -> `data/tables/supp_table_s7_ll37_truncation_primary_hcs.csv`
- Length-bucketed HCS is reported as the primary value because short peptides can share many non-specific 3-mers with longer sequences. The unbucketed sensitivity analysis used the same Config G model and training predictions but searched all training sequences with non-zero 3-mer Jaccard. Absolute HCS scores decreased under unbucketed search because many additional weakly similar sequences were included. The monotonic rank order among the three experimentally active LL-37 variants was unchanged. -> `data/tables/supp_table_s7b_ll37_bucketed_vs_unbucketed_hcs.csv`
- HCS was applied to 10 pairs of 20 peptides from the externally published AMP activity-cliff benchmark of Li et al. [47]. These peptide pairs differ by a single conservative amino-acid substitution and have experimental MIC values against S. aureus. Diagnostics used configuration G (ampmodel_single_1280d) and length-bucketed k-mer Jaccard (k=3). Activity rank denotes the low-MIC or high-MIC member within each published peptide pair; it is not used as a binary active/inactive label. -> `data/tables/supp_table_s8_ampcliff_hcs_summary.csv`
- Supplementary Table S9. Cross-pLM curve-span summary. -> `data/tables/supp_table_s9_cross_plm_curve_spans.csv`
- Supplementary Table S10. Threshold-level curve data for cross-pLM analysis. -> `data/tables/supp_table_s10_cross_plm_threshold_data.csv`
- Supplementary Table S11. Source-held-out curve-span and intervention-effect summary. -> `data/tables/supp_table_s11_source_heldout_summary.csv`
- Supplementary Table S12. Threshold-level curve data for source-held-out analysis. -> `data/tables/supp_table_s12_source_heldout_threshold_data.csv`
- Supplementary Table S13. Per-seed source-held-out results. -> `data/tables/supp_table_s13_source_heldout_per_seed.csv`
- Supplementary Table S14. GRL lambda-sweep summary. -> `data/tables/supp_table_s14_grl_lambda_sweep.csv`
- Supplementary Table S15. HCS-E alpha-sweep summary. -> `data/tables/supp_table_s15_hcse_alpha_sweep.csv`
- Supplementary Table S16. Threshold-level curve data for HCS-E. -> `data/tables/supp_table_s16_hcse_threshold_data.csv`
- Supplementary Table S17. Summary statistics for the fixed-model application demonstration. -> `data/tables/supp_table_s17_candidate_pool_summary.csv`
- Supplementary Table S18. Similarity composition of the raw and audited Top 20 candidates. -> `data/tables/supp_table_s18_candidate_top20_summary.csv`
- Supplementary Table S19. Candidates whose Top-20 membership changed after the similarity constraint. -> `data/tables/supp_table_s19_changed_candidates.csv`

## License and reuse

- Code in this repository is released under the MIT License.
- Derived result tables remain subject to the license and reuse conditions of the original source databases when those conditions apply.
- This repository does not grant rights to redistribute third-party raw database records.

## Data and code availability text

Suggested manuscript text is provided in `docs/data_code_availability_statement.md`.
