# Developer Guide

## Prerequisites

- Python version supported by `pyproject.toml`
- Git
- A terminal or command prompt

## Set up the environment

Clone the repository:

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd agentops-intelligence
```

Create and activate a virtual environment.

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the project:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

If the optional `dev` dependency group is not configured, install the test and development dependencies using the current `pyproject.toml`.

## Run tests

```bash
pytest
```

Run the tests after changes to the engine, registry, policy, verification, or tool implementations.

## Run the benchmark

```bash
python benchmarks/run_benchmark.py
```

Inspect the benchmark's output and confirm that the reported metrics match the current evaluation logic.

## Development guidelines

### Adding a tool

1. Define the tool's intended inputs and outputs.
2. Implement argument validation.
3. Register the tool through the existing registry.
4. Add tests for valid and invalid inputs.
5. Add policy tests if the tool requires restrictions.
6. Add verification cases where relevant.
7. Update the README and architecture documentation if behavior changes.

### Changing policy behavior

- Document the rule and its purpose.
- Add tests for both permitted and denied requests.
- Check that denied operations are not executed.
- Test interactions between rules.
- Avoid silently weakening default restrictions.

### Changing verification behavior

- Define the expected condition explicitly.
- Include passing and failing examples.
- Test malformed and missing outputs.
- Document what the verifier does not check.
- Avoid describing a narrow check as proof of general correctness.

## Code quality

- Prefer small, explicit functions.
- Keep policy decisions separate from tool implementations.
- Use structured outcomes rather than ambiguous success messages.
- Avoid embedding secrets or environment-specific paths.
- Add regression tests for fixed defects.
- Preserve benchmark comparability when changing evaluation logic.

## Branching workflow

Use focused branches such as:

- `docs/project-documentation`
- `test/benchmark-expansion`
- `feat/agent-planner`
- `feat/audit-logging`

Create changes on a feature branch, run relevant tests, and open a pull request into `main`.

## Troubleshooting

### Installation fails

Check the active Python interpreter and inspect `pyproject.toml` for supported versions and dependency groups.

### Tests fail

Read the first failure, reproduce it independently, and check whether the failure comes from the code, environment, or a changed expectation.

### Benchmark results change

Check for changes to the dataset, tool behavior, expected outcomes, metric definitions, or configuration. Document any intentional change.

## Before submitting changes

- [ ] Tests pass.
- [ ] New behavior has tests.
- [ ] Documentation is updated.
- [ ] No secrets or local environment files are committed.
- [ ] Benchmark changes are documented.
- [ ] Research claims are supported by evidence.
