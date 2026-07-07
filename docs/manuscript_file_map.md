# Manuscript file map

This note maps the main manuscript display items and supplementary tables to the corresponding repository files.

## Main figures

- Figure 1 -> `data/figure_source/figure1_threshold_profile.csv`, `data/figure_source/figure1_auc_profile.csv`, `scripts/make_figure1.m`
- Figure 2 -> `data/figure_source/figure2_source_heldout_profiles.csv`, `data/figure_source/figure2_endpoint_spans.csv`, `data/figure_source/figure2_retraining_changes.csv`, `scripts/make_figure2.m`
- Figure 3 -> `data/figure_source/figure3_unique_candidate_pool_summary.csv`, `data/figure_source/figure3_candidate_pool_points.csv`, `data/figure_source/figure3_raw_top20.csv`, `data/figure_source/figure3_audited_top20.csv`, `data/figure_source/figure3_similarity_composition.csv`, `scripts/make_figure3.m`

## Main manuscript tables

- Table 1 -> `data/tables/table1_data_flow.csv`
- Table 2 -> `data/tables/table2_ablation_clean_retraining.csv`
- Table 3 -> `data/tables/table3_threshold_retained_subset.csv`
- Table 4 -> `data/tables/table4_prevalence_matched_ap.csv`

## Supplementary tables

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

## Current manuscript extension summaries

- DeepLoc multitask external contrast -> `results/extensions/deeploc_multitask_summary.json`
- DeepLoc clean-retraining bridge -> `results/extensions/deeploc_clean_retrain_bridge_results.json`
- Full ESCAPE multilabel threshold profiles -> `results/extensions/full_escape_multilabel_profile_results.json`
- Full ESCAPE multilabel clean-retraining branch -> `results/extensions/full_escape_multilabel_clean_retrain_results.json`
- Broader raw-filtered ESCAPE labelwise extension -> `results/extensions/multilabel_extension_results.json`
- TAPE fluorescence boundary case -> `results/extensions/tape_fluorescence_formal_results.json`
- Remote homology family-holdout benchmark -> `results/extensions/remote_homology_family_results.json`
- Controlled similarity-mixture simulation -> `results/extensions/controlled_similarity_mixture_results.json`
- Bridge-level summary across case families -> `results/extensions/bridge_statistics_summary.json`
