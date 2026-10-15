# Contributing to AgentOps Intelligence

Thank you for your interest in contributing.

Contributions can improve the execution engine, policy enforcement, verification, tests, benchmark, and documentation.

## Before contributing

- Read `README.md`.
- Review `docs/architecture.md`.
- Review `docs/policy-and-verification.md` for changes affecting enforcement or correctness.
- Check existing issues and pull requests if the repository uses them.

## Development setup

Clone the repository and create a virtual environment:

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd agentops-intelligence
python -m venv .venv
```

Activate the environment.

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
source .venv/bin/activate
```

Install the project according to its current configuration:

```bash
python -m pip install -e ".[dev]"
```

If the optional development dependency group is unavailable, follow the dependency instructions in `pyproject.toml`.

## Branch naming

Use descriptive branch names:

- `docs/<description>`
- `test/<description>`
- `fix/<description>`
- `feat/<description>`

Examples:

- `docs/project-documentation`
- `test/benchmark-expansion`
- `fix/verification-edge-case`
- `feat/multi-step-execution`

## Making changes

1. Create a branch from the current `main`.
2. Make a focused change.
3. Add tests for new behavior or defects.
4. Run the relevant tests.
5. Update documentation.
6. Inspect the final diff for accidental files or secrets.
7. Open a pull request describing the change.

## Testing

Run the test suite:

```bash
pytest
```

Run the benchmark when changes may affect execution outcomes or evaluation:

```bash
python benchmarks/run_benchmark.py
```

Use the actual configured project commands if these entry points change.

## Contribution guidelines

### Execution engine

Keep control flow explicit and preserve clear distinctions between successful execution, policy denial, and failure.

### Policy enforcement

Add tests for allowed and denied cases. Verify that denied operations do not execute.

### Verification

Define expected conditions clearly. Include tests for both correct and incorrect outputs.

### Benchmark

Document dataset changes and metric definitions. Do not compare results from incompatible datasets without explaining the differences.

### Documentation

Describe existing behavior accurately. Label future functionality as planned rather than implemented.

## Pull request checklist

- [ ] The change has a clear purpose.
- [ ] Relevant tests have been added or updated.
- [ ] Tests pass locally.
- [ ] Documentation has been updated.
- [ ] No credentials or secrets have been committed.
- [ ] Benchmark changes are explained.
- [ ] Limitations and compatibility impacts are documented.

## Research integrity

Do not present preliminary or synthetic benchmark results as proof of general reliability, novelty, or statistical significance.

## Questions and suggestions

Open an issue or discussion in the repository if those features are enabled. Describe the problem, expected behavior, and a minimal reproducible example where possible.
