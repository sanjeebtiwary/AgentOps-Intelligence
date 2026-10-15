---
name: Feature request
about: Propose a new tool, policy rule, verification check, benchmark case or other improvement
title: "[Feature] "
labels: enhancement
assignees: ""
---

## Problem or motivation

What limitation or failure mode does this address? Link the relevant roadmap phase if one applies
(see [`docs/roadmap.md`](../../docs/roadmap.md)).

## Proposed change

Describe what you would like to see.

## Type of change

- [ ] New tool
- [ ] Policy rule
- [ ] Verification check / postcondition
- [ ] Benchmark cases or metrics
- [ ] Planner interface / multi-step execution
- [ ] Optional LLM integration
- [ ] API / operations
- [ ] Documentation
- [ ] Other:

## Safety and correctness considerations

- Can this change weaken existing policy restrictions? How is that prevented?
- Can it let a caller bypass the execution engine?
- How will it be tested (permitted and denied cases, malformed inputs, verification failures)?
- What will the verifier or policy **not** cover?

## Evaluation impact

Would this change benchmark behavior or metric definitions? If so, how will comparability be preserved?

## Alternatives considered

Other approaches and why you prefer this one.

## Willing to contribute?

- [ ] I can open a pull request for this
- [ ] I would like guidance first
