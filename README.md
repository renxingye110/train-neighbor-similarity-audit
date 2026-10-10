# Train-neighbor similarity diagnostic

This repository provides the core P/A/S diagnostic for fixed protein-sequence predictions and a runnable TAPE remote-homology analysis with matched clean retraining.

The workflow builds train-to-test 3-mer neighborhoods, computes the performance profile P and label-geometry axis A, then applies the frozen support gate S. The TAPE runner also refits after the Jaccard-0.40 training filter to calculate the held-out retraining change R.

## Run the diagnostic

Use Python 3.10 or later. Install the dependencies and run the unit tests:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests
```

For a fixed binary-classifier output, prepare two CSV files:

- `train.csv`: `sequence,label`, with labels encoded as 0 or 1.
- `test.csv`: `sequence,label,score`, where `score` is the fixed model's probability for class 1.

Run the profile, label-geometry, and support-gate calculation:

```bash
python scripts/run_fixed_prediction_audit.py --train train.csv --test test.csv --output-dir audit_output
```

The command writes `profile.csv` and `diagnostic.json`. The default profile span uses the `<0.40` and `<1.00` retained sets. The primary ESCAPE profile can be selected with `--profile-span 0.30 1.00`. Use `--geometry-weighting class_balanced` for an equal mean across the two classes. Equal-similarity neighbors are ordered by their training-row index.

## Reproduce the TAPE screen

Obtain the TAPE remote-homology JSON data from the [official TAPE repository](https://github.com/songlab-cal/tape). Place `remote_homology_train.json`, `remote_homology_valid.json`, and `remote_homology_test_family_holdout.json` in one directory, then run:

```bash
python scripts/reproduce_tape_screen.py --data-dir /path/to/remote_homology --output-dir tape_output
```

This fits the one-vs-rest 3-mer logistic models on the supplied training and validation records, evaluates the fixed profiles, refits after the Jaccard-0.40 clean-training filter, and checks the seven endpoint results against Supplementary Table S3 using the tolerances recorded in the output. The frozen thresholds and support criteria are in `configs/released_analysis.json`.

## Files

- `src/benchmark_diagnostic.py`: Jaccard neighborhoods, performance profiles, label geometry, and support gate.
- `scripts/run_fixed_prediction_audit.py`: command-line interface for fixed predictions.
- `scripts/reproduce_tape_screen.py`: end-to-end TAPE one-vs-rest and clean-retraining analysis.
- `data/tables/` and `data/figure_source/`: manuscript tables and numerical figure inputs.
- `results/primary_generalization_summary.json`: released endpoint summary.

Inputs are obtained from the ESCAPE, TAPE, and ESM-2 sources cited in the manuscript. The repository contains the analysis code and derived manuscript tables.

## Citation and license

Please cite the accompanying manuscript and the repository commit linked in its Data Availability statement. Code is released under the MIT License. Derived tables remain subject to the terms of their source databases where applicable.
