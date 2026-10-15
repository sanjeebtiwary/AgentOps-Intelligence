# Project Roadmap

This roadmap distinguishes the existing prototype from planned development. Check each item against the current code before marking it complete.

## Phase 1 — Deterministic Core

**Goal:** Establish a small, testable execution foundation.

- [x] Implement a basic execution engine
- [x] Register deterministic utility tools
- [x] Add policy enforcement
- [x] Add outcome verification
- [x] Create an initial synthetic benchmark
- [x] Add automated tests

## Phase 2 — Benchmark Reliability

**Goal:** Make reliability claims measurable and reproducible.

- [ ] Expand the dataset with positive and negative cases
- [ ] Define all metric denominators
- [ ] Separate policy denials from execution errors
- [ ] Measure verification precision and recall
- [ ] Add failure-category reporting
- [ ] Record dataset and code versions
- [ ] Add ablation experiments
- [ ] Document limitations and reproducibility steps

## Phase 3 — Multi-Step Execution

**Goal:** Evaluate workflows involving more than one tool call.

- [ ] Define a task and step representation
- [ ] Track dependencies between steps
- [ ] Handle failed intermediate steps
- [ ] Define stop conditions
- [ ] Verify intermediate and final outcomes
- [ ] Add multi-step benchmark cases

## Phase 4 — Planner Interface

**Goal:** Introduce planning while preserving execution controls.

- [ ] Define a planner interface
- [ ] Separate planning from execution
- [ ] Validate planner-generated tool requests
- [ ] Prevent planner bypass of policy enforcement
- [ ] Test invalid and adversarial tool requests
- [ ] Compare planned workflows with deterministic test cases

## Phase 5 — Optional LLM Integration

**Goal:** Explore LLM-based planning without making the core dependent on a paid model.

- [ ] Define an interchangeable model-provider interface
- [ ] Evaluate a local or optional model
- [ ] Validate generated tool arguments
- [ ] Record planning and execution outcomes separately
- [ ] Compare model-assisted and deterministic workflows
- [ ] Document resource requirements and limitations

## Phase 6 — API and Operations

**Goal:** Make the prototype easier to demonstrate and integrate.

- [ ] Design an API contract
- [ ] Add request validation and structured responses
- [ ] Add authentication where deployment requires it
- [ ] Introduce bounded execution time and resource use
- [ ] Add structured audit events
- [ ] Add deployment documentation
- [ ] Perform security and reliability testing

## Completion criteria

A roadmap item should be marked complete only after:

1. The functionality is implemented.
2. Relevant tests pass.
3. Documentation reflects actual behavior.
4. Known limitations are recorded.
5. Benchmark changes are reproducible where applicable.

A completed roadmap item does not, by itself, establish research novelty or production readiness.