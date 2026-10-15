# AgentOps Intelligence

**A deterministic execution and evaluation core for tool-using AI workflows.**

AgentOps Intelligence is a Python research prototype that separates AI-generated plans from the runtime responsible for authorizing, executing, and verifying tool calls.

The goal is to make tool-using AI workflows more **controlled, auditable, and measurable**.

> **Project status:** Early-stage prototype. The included tools and benchmark are small and deterministic. This project does not claim production readiness or establish research superiority.

## Key Features

- **Deterministic execution core:** Executes structured plans in a defined order and records step outcomes.
- **Policy enforcement:** Applies an explicit tool allowlist, argument validation, step limits, and optional approval requirements.
- **Verification engine:** Checks tool outputs against explicit postconditions and fails closed when checks fail.
- **Audit events:** Records run lifecycle, policy decisions, tool outcomes, and verification results in memory.
- **Synthetic benchmark:** Compares a baseline without postcondition checks against policy-plus-verification mode.
- **Automated tests:** Tests normal execution, invalid arguments, unknown tools, and verification failures.

## Architecture

```text
Structured Plan
      |
      v
 Plan Validation
      |
      v
 Policy Enforcement
      |
      +---- Denied ----> Block + Audit Event
      |
      v
  Tool Registry
      |
      v
 Deterministic Tool
      |
      v
    Output
      |
      v
 Verification Engine
      |
      +---- Failed ----> Run Failed
      |
      v
   Run Result
```

The plan is structured data, not executable code. Only registered and allowlisted tools can be invoked. A tool returning successfully does not automatically mean the task succeeded; verification evaluates its output separately.

## Technology Stack

- Python 3.10+
- Python standard library for the execution core
- pytest for automated tests
- Optional FastAPI and Uvicorn dependencies for future API development

The current implementation does not require a paid API key, cloud service, or external LLM.

## Project Structure

```text
agentops-intelligence/
├── data/
│   └── benchmark_cases.jsonl
├── reports/
├── src/
│   └── agentops/
│       ├── benchmark/
│       │   ├── cases.py
│       │   └── runner.py
│       ├── tools/
│       │   ├── math_tools.py
│       │   └── text_tools.py
│       ├── engine.py
│       ├── models.py
│       ├── policy.py
│       ├── registry.py
│       └── verification.py
├── tests/
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
```

## Getting Started

### Requirements

Install Python 3.10 or newer.

Check your Python version:

```bash
python --version
```

### 1. Clone the repository

```bash
git clone https://github.com/sanjeebtiwary/AgentOps-Intelligence
cd agentops-intelligence
```

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

### 4. Run tests

```bash
pytest
```

### 5. Run the benchmark

Run from the repository root:

```bash
python -m agentops.benchmark.runner \
  --dataset data/benchmark_cases.jsonl \
  --out reports
```

If the package has not been installed, use `PYTHONPATH`:

**Windows PowerShell**

```powershell
$env:PYTHONPATH = "src"
python -m agentops.benchmark.runner --dataset data/benchmark_cases.jsonl --out reports
```

**macOS/Linux**

```bash
PYTHONPATH=src python -m agentops.benchmark.runner --dataset data/benchmark_cases.jsonl --out reports
```

The benchmark generates:

- `reports/benchmark_results.csv`
- `reports/benchmark_results.json`

## Included Tools

| Tool | Description |
|---|---|
| `add` | Adds two finite, bounded numbers |
| `multiply` | Multiplies two finite, bounded numbers |
| `divide` | Divides two finite, bounded numbers and rejects division by zero |
| `normalize_text` | Normalizes whitespace |
| `word_count` | Counts whitespace-separated words |

## Verification Checks

The verification engine supports:

- `exists` — checks whether a path exists and is not null.
- `equals` — compares a value with an expected value.
- `type_is` — checks a supported JSON-like data type.
- `numeric_range` — checks a numeric value against optional bounds.
- `contains` — checks whether a string, list, or dictionary contains a value.

Unsupported verification checks fail closed rather than being silently ignored.

## Policy Enforcement

The policy engine provides:

- Explicit tool allowlisting.
- A maximum number of steps per plan.
- Required-argument and type validation.
- Rejection of undeclared arguments unless permitted by a tool.
- Optional approval requirements for selected tools.

The approval-token mechanism is a prototype demonstration, not enterprise-grade authorization.

## Benchmark and Research

The included benchmark is a small synthetic smoke-test dataset covering normal operations, malformed inputs, unknown tools, tool errors, and verification failures.

It reports:

- Run success rate.
- Expected-outcome accuracy.
- Policy denial count.
- Verification failure count.
- Mean local execution latency.
- Per-case outcomes.

These results are intended to validate the benchmark mechanics, not prove general effectiveness. A credible research evaluation requires a larger curated dataset, held-out cases, adversarial testing, repeated trials, and uncertainty estimates.

## Limitations and Security

This is an early-stage prototype, not a hardened production agent platform.

- Tools execute in the same Python process.
- Persistent database-backed audit storage is not implemented.
- Authentication and enterprise approval workflows are not implemented.
- An LLM planner and web API are not implemented in this milestone.
- Distributed execution, robust cancellation, and isolated tool execution are not implemented.

Do not register arbitrary shell commands, generated-code execution, or high-impact external actions without an appropriate isolation and authorization boundary. Never commit secrets, credentials, or private data.

## Roadmap

1. Add persistent run and event storage.
2. Implement a FastAPI service for creating runs and retrieving results.
3. Integrate an LLM planner that emits validated structured plans.
4. Add stronger isolation for external and high-impact tools.
5. Expand the benchmark with held-out and adversarial cases.
6. Evaluate repeated trials and report uncertainty and failure categories.

## License

See [`LICENSE`](LICENSE) for the license text included in this repository. Confirm that the chosen license matches your intended distribution and any third-party dependencies before publishing.
