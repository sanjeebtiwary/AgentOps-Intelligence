---
name: Bug report
about: Report incorrect behavior in execution, policy, verification, tools or the benchmark
title: "[Bug] "
labels: bug
assignees: ""
---

> **Security issue?** Do not file it here. Follow [`SECURITY.md`](../../SECURITY.md) instead.

## Summary

A clear, one- or two-sentence description of the bug.

## Component

- [ ] Execution engine
- [ ] Tool registry
- [ ] Policy engine
- [ ] Verification
- [ ] Tool implementation (which tool?): 
- [ ] Benchmark / metrics
- [ ] Documentation
- [ ] Other:

## Steps to reproduce

A minimal snippet or command is ideal.

```python
from agentops import ExecutionEngine, PolicyEngine, ToolRequest, build_default_registry, default_verifier

engine = ExecutionEngine(build_default_registry(), PolicyEngine(), default_verifier())
print(engine.execute(ToolRequest("add", {"a": 1, "b": 2})))
```

## Expected behavior

What should have happened? If relevant, name the expected `Status`
(`SUCCESS`, `INVALID_REQUEST`, `UNKNOWN_TOOL`, `POLICY_DENIED`, `EXECUTION_FAILURE`, `VERIFICATION_FAILURE`).

## Actual behavior

What happened instead? Include the full `Outcome`, traceback or benchmark output.

```text
paste output here
```

## Does a denied action reach tool execution?

- [ ] Not applicable
- [ ] No, the tool did not run
- [ ] Yes, a policy-denied request executed (please also report privately if this is exploitable)

## Environment

- AgentOps Intelligence version / commit:
- Python version:
- OS:
- Installed with: `pip install -e ".[dev]"` / other:

## Additional context

Anything else that helps: related issues, benchmark dataset version, configuration used.
