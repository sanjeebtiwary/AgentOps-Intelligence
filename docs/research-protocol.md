# Research Protocol

## 1. Research motivation

Tool-using AI agents introduce multiple sources of failure: planning errors, invalid tool calls, policy violations, execution errors, and incorrect final outcomes.

AgentOps Intelligence provides a controlled prototype for studying whether explicit policy enforcement and independent verification can improve measurable aspects of execution reliability.

## 2. Research questions

**RQ1:** How does policy enforcement affect the rate of disallowed tool actions?

**RQ2:** How accurately does independent verification identify incorrect tool results?

**RQ3:** What trade-offs arise between outcome correctness and task completion?

**RQ4:** What execution overhead is introduced by policy enforcement and verification?

**RQ5:** How do these effects change as task complexity and the number of execution steps increase?

These questions are proposed directions, not established findings.

## 3. Experimental conditions

A useful experimental design should compare clearly specified configurations:

- **C0 — Baseline:** A documented baseline without the intervention being evaluated.
- **C1 — Policy only:** Baseline plus policy enforcement.
- **C2 — Verification only:** Baseline plus verification.
- **C3 — Policy and verification:** Both interventions enabled.

The actual implementation must support each configuration before it can be evaluated. If the current benchmark only supports two configurations, implement and test the additional conditions before reporting them.

## 4. Independent and dependent variables

Potential independent variables:

- Policy enforcement enabled or disabled
- Verification enabled or disabled
- Task complexity
- Number of tool calls
- Tool error conditions

Potential dependent variables:

- Task success rate
- Expected-outcome accuracy
- Policy violation rate
- Verification precision and recall
- Execution latency
- Failure-detection rate

Define each variable operationally before collecting results.

## 5. Dataset requirements

The evaluation dataset should include valid and invalid tool requests, policy-denied actions, correct and incorrect outputs, and execution failures.

For each test case, preserve:

- Unique case identifier
- Task description
- Input arguments
- Expected action or result
- Policy ground truth
- Expected verification outcome
- Task-level success criteria
- Failure category

Separate development cases from held-out evaluation cases when appropriate to reduce tuning bias.

## 6. Ground truth

Ground truth should be defined independently of the system being evaluated.

For example, if the verifier claims that an output is incorrect, the benchmark needs a separate criterion for determining whether that claim is true.

Do not use the verifier's own decision as the sole ground truth for measuring verifier accuracy.

## 7. Threats to validity

### Construct validity

Metrics such as task success and verification failure may not capture every aspect of agent reliability.

### Internal validity

Differences in configuration, test order, dependencies, or implementation may affect results.

### External validity

Synthetic utility-tool tasks may not represent complex agent workflows, external APIs, or real-world environments.

### Measurement validity

Incorrect expected values or inconsistent metric denominators can produce misleading results.

### Reproducibility

Changes in code, datasets, or evaluation rules can make runs incomparable unless versions are recorded.

## 8. Reporting requirements

Every report should include:

- Research question
- Hypothesis, if applicable
- Configuration details
- Dataset composition
- Metric definitions
- Sample size
- Results for each configuration
- Failure analysis
- Variability or uncertainty, where relevant
- Limitations
- Reproduction instructions

Report findings that do not support the original hypothesis as well as positive results.

## 9. Research integrity

Do not claim novelty, statistical significance, general reliability improvements, or superiority over other systems without appropriate evidence.

The initial benchmark is preliminary. Further experiments are needed before drawing broader conclusions.