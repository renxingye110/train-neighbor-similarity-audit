# Data dictionary

## Figure source files

- `figure1_threshold_profile.csv`: threshold-specific mAP values for the ESCAPE reference profile shown in Figure 1.
- `figure1_auc_profile.csv`: threshold-specific AUC values for the inset in Figure 1.
- `figure2_source_heldout_profiles.csv`: threshold-level source-held-out profile data across ESCAPE, DRAMP, APD6, and DBAASP.
- `figure2_endpoint_spans.csv`: endpoint span summary used for the left comparison panel in Figure 2.
- `figure2_retraining_changes.csv`: clean-fold retraining change summary used for the right comparison panel in Figure 2.
- `figure3_unique_candidate_pool_summary.csv`: candidate-pool summary for the retrospective prioritization example.
- `figure3_candidate_pool_points.csv`: full unique-sequence candidate pool used for the Figure 3 scatter panel.
- `figure3_raw_top20.csv`: the raw Top 20 candidate list before the Jaccard constraint.
- `figure3_audited_top20.csv`: the Top 20 candidate list after the Jaccard constraint.
- `figure3_similarity_composition.csv`: low/medium/high similarity counts for the raw and audited Top 20 lists.
- `figure3_replaced_candidates.csv`: representative candidates whose Top-20 membership changed.

## Table exports

The `data/tables/` directory contains CSV exports of the current manuscript tables. The exported files preserve the visible table headers and cell text from the source DOCX files. Any abbreviations remain defined by the manuscript captions and surrounding text.
