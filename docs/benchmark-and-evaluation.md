# Benchmark and Evaluation

## 1. Purpose

The benchmark evaluates the behavior of AgentOps Intelligence under a small collection of synthetic tool-use cases.

Its initial purpose is to provide a repeatable smoke test and a starting point for studying the effects of policy enforcement and verification.

It is not a comprehensive benchmark of autonomous agents.

## 2. Configurations

The initial comparison includes:

- **Baseline:** The benchmark's baseline execution configuration.
- **Policy + verification:** A stricter configuration that applies policy enforcement and verification.

Consult the benchmark implementation to determine precisely which components are enabled in each configuration.

## 3. Preliminary results

One initial run reported:

| Metric | Baseline | Policy + verification |
|---|---:|---:|
| Expected-outcome accuracy | 81.82% | 100% |
| Task success rate | 54.55% | 36.36% |

The stricter configuration also reported two verification failures.

These figures are preliminary observations from a small synthetic dataset. They should not be treated as statistically significant findings or generalized to real-world AI agents.

### Results from the dataset in this repository

`benchmarks/cases.py` (`synthetic-v1`, 14 cases) is run by `benchmarks/run_benchmark.py` across four configurations (baseline, policy only, verification only, policy + verification). Metric denominators are defined in `benchmarks/metrics.py`. Task success rate here means "the request ended in `SUCCESS`" (a result was returned and, if verification is on, accepted); the separate *silent error rate* counts accepted results that differ from ground truth.

The ground truth and the verifier were written together on a tiny dataset, so 100% expected-outcome accuracy for the full configuration is largely by construction. The numbers above in this section come from an earlier run and will not match this dataset exactly.

## 4. Why metrics differ

Expected-outcome accuracy and task success rate measure different properties.

A configuration can detect or reject an incorrect result more reliably while also completing fewer tasks. Consequently, improving one metric does not necessarily improve all measures of system performance.

Policy denials and verification failures must be interpreted in relation to the intended task and the benchmark's ground truth.

## 5. Metrics to report

### Expected-outcome accuracy

The fraction of evaluated cases for which the observed outcome matches the defined expected outcome.

The benchmark must specify whether policy denials, execution failures, and verification failures count as correct outcomes for a particular case.

### Task success rate

The fraction of evaluated tasks that meet the benchmark's task-level success criteria.

### Policy violation rate

The proportion of applicable evaluated actions that violate the benchmark's defined policy requirements.

Define the denominator explicitly. Do not count a correctly denied request as an executed policy violation.

### Verification failure rate

The fraction of results evaluated by the verifier that fail its configured checks.

This metric alone does not reveal whether the verifier correctly detected an error. Some failures may be false positives.

### Verification recall

The fraction of genuinely incorrect results that the verifier correctly identifies.

### Verification precision

The fraction of verifier-reported failures that are genuinely incorrect according to the benchmark ground truth.

### Execution overhead

The additional time or computational cost introduced by policy checks and verification compared with a defined baseline.

## 6. Dataset design

Future benchmark cases should include:

- Valid tool requests
- Invalid arguments
- Unknown tools
- Policy-permitted actions
- Policy-denied actions
- Correct results
- Incorrect results
- Tool execution errors
- Verification false positives
- Verification false negatives
- Multi-step tasks

Each case should specify its inputs, expected behavior, ground-truth outcome, and the metrics to which it contributes.

## 7. Reproducibility

For each benchmark run, record:

- Repository revision or commit
- Python version
- Configuration
- Dataset version
- Metric definitions
- Number of cases
- Raw outcomes
- Aggregate results
- Any exclusions or errors

Use the same dataset and metric definitions when comparing configurations. If the dataset or metric logic changes, identify the change in the report.

## 8. Experimental protocol

A future evaluation should:

1. Define hypotheses before running experiments.
2. Define the benchmark cases and ground truth.
3. Specify baseline and intervention configurations.
4. Fix the metric definitions and denominators.
5. Run all configurations on comparable cases.
6. Inspect failures and disagreements.
7. Repeat experiments where variability exists.
8. Report negative results and limitations.
9. Publish sufficient detail for independent reproduction.

## 9. Current limitations

- The dataset is small and synthetic.
- Results may be sensitive to the specific cases selected.
- A single run cannot establish statistical significance.
- Narrow verification rules may inflate apparent accuracy.
- The benchmark does not establish performance on production workloads.

## 10. Interpreting results

Treat the current benchmark as a development aid. Stronger research claims require a broader dataset, carefully defined ground truth, appropriate baselines, transparent metrics, and reproducible experiments.
