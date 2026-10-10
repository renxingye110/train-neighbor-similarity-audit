# Data dictionary

## Figure source files

- `figure1_threshold_profile.csv`: threshold-specific mAP values for the ESCAPE reference profile shown in Figure 1.
- `figure1_auc_profile.csv`: threshold-specific AUC values for the inset in Figure 1.
- `figure2_primary_endpoint_summary.csv`: complete eight-endpoint primary screen used to derive the released-case Figure 2 comparison.
- `figure3_released_case_summary.csv`: the four released primary cases used in Figure 3.
- `supp_figure_s1_primary_endpoint_screen.csv`: complete primary endpoint values for Supplementary Figure S1.
- `supp_figure_s2_proxy_bins.csv`: bin-level Needleman-Wunsch identity summary for Supplementary Figure S2.

## Table exports

The `data/tables/` directory contains CSV exports of Table 1 and Supplementary Tables S1-S6. Numeric uncertainty entries use ASCII `+/-` notation for portability across spreadsheet and command-line tools. Abbreviations are defined in the manuscript captions and surrounding text.

## Analysis code

- `src/benchmark_diagnostic.py` implements the train-neighbor profile, chance-corrected label geometry, and support gate.
- `scripts/run_fixed_prediction_audit.py` accepts training sequences and labels plus test sequences, labels, and fixed scores.
- `scripts/reproduce_tape_screen.py` reruns the TAPE one-vs-rest models and clean-retraining comparison from the three TAPE JSON split files.
- `configs/released_analysis.json` records the thresholds, support criteria, and model settings used for the released analysis.
