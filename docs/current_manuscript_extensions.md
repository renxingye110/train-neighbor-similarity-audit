# Current manuscript extensions

This note lists the additional packaged summaries that support the current JBI manuscript beyond the original Figure 1-3 release set.

These files are intentionally lightweight. They document the reported extension analyses without turning this repository into a full retraining dump.

## Extension summaries in `results/extensions/`

- `bridge_statistics_summary.json`
  Small bridge-level correlation summary used to describe how larger post hoc spans tend to align with larger matched retraining effects across the packaged case families.

- `deeploc_multitask_summary.json`
  Five-task DeepLoc 2.0 profile summary used as a low-effect external contrast.

- `deeploc_clean_retrain_bridge_results.json`
  DeepLoc 2.0 clean-retraining bridge summary used to compare low-span post hoc behavior with matched retraining changes.

- `full_escape_multilabel_profile_results.json`
  Full ESCAPE multilabel profile summary across the retained threshold series.

- `full_escape_multilabel_clean_retrain_results.json`
  Matched clean-retraining summary for the full ESCAPE multilabel branch.

- `multilabel_extension_results.json`
  Broader raw-filtered ESCAPE labelwise extension summary used to support the partial multilabel discussion.

- `tape_fluorescence_formal_results.json`
  TAPE fluorescence boundary-case summary in the high-similarity regression setting.

- `remote_homology_family_results.json`
  TAPE remote homology family-holdout summary used as a more intermediate independent non-AMP benchmark.

- `controlled_similarity_mixture_results.json`
  Controlled similarity-mixture simulation summary showing how span-style statistics increase as high-similarity exposure increases.

## Scope boundary

These JSON summaries are provided for inspection, comparison, and manuscript traceability.

This repository still does **not** include:

- full raw third-party benchmark dumps
- embedding caches
- model checkpoints
- complete retraining pipelines for every extension branch

The repository remains a compact reproducibility package aligned to the manuscript rather than a full local project mirror.
