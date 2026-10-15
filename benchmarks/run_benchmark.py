"""Run the synthetic benchmark across four configurations.

Usage:  python benchmarks/run_benchmark.py [--repeats N] [--json PATH]
"""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
try:
    import agentops  # noqa: F401
except ImportError:  # allow running from a fresh checkout without installing
    sys.path.insert(0, str(ROOT / "src"))

from cases import CASES, DATASET_VERSION, benchmark_registry, register_benchmark_postconditions  # noqa: E402
from metrics import compute_metrics  # noqa: E402

from agentops import ExecutionEngine, PolicyEngine, default_verifier  # noqa: E402

CONFIGS = {  # name -> (policy enabled, verification enabled)
    "baseline": (False, False),
    "policy_only": (True, False),
    "verification_only": (False, True),
    "policy_verification": (True, True),
}


def build_engine(policy: bool, verify: bool) -> ExecutionEngine:
    verifier = None
    if verify:
        verifier = default_verifier()
        register_benchmark_postconditions(verifier)
    return ExecutionEngine(benchmark_registry(), PolicyEngine() if policy else None, verifier)


def run_config(name: str, repeats: int) -> dict:
    policy, verify = CONFIGS[name]
    engine = build_engine(policy, verify)
    pairs = [(case, engine.execute(case.request)) for case in CASES]
    # Timing: mean wall time over `repeats` passes (outcomes are deterministic).
    start = time.perf_counter()
    for _ in range(repeats):
        for case in CASES:
            engine.execute(case.request)
    mean_us = (time.perf_counter() - start) / (repeats * len(CASES)) * 1e6
    metrics = compute_metrics(pairs, verifier_enabled=verify)
    metrics["mean_time_per_case_us"] = mean_us
    raw = [
        {
            "case": c.id,
            "expected": c.expected_status.value,
            "observed": o.status.value,
            "result": repr(o.result) if o.result is not None else None,
            "error": o.error,
        }
        for c, o in pairs
    ]
    return {"policy": policy, "verification": verify, "metrics": metrics, "raw": raw}


def git_revision() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, stderr=subprocess.DEVNULL, text=True
        ).strip()
    except Exception:  # noqa: BLE001
        return None


def fmt(v, kind="pct") -> str:
    if v is None:
        return "n/a"
    return f"{v * 100:.2f}%" if kind == "pct" else f"{v:.1f}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repeats", type=int, default=200, help="timing passes per configuration")
    ap.add_argument("--json", type=Path, default=ROOT / "benchmarks" / "results" / "latest.json")
    args = ap.parse_args()

    results = {name: run_config(name, args.repeats) for name in CONFIGS}
    meta = {
        "dataset_version": DATASET_VERSION,
        "cases": len(CASES),
        "repeats": args.repeats,
        "python": platform.python_version(),
        "git_revision": git_revision(),
    }

    rows = [
        ("Expected-outcome accuracy", "expected_outcome_accuracy", "pct"),
        ("Task success rate", "task_success_rate", "pct"),
        ("Silent error rate", "silent_error_rate", "pct"),
        ("Policy violation rate", "policy_violation_rate", "pct"),
        ("Verification failure rate", "verification_failure_rate", "pct"),
        ("Verification precision", "verification_precision", "pct"),
        ("Verification recall", "verification_recall", "pct"),
        ("Mean time per case (us)", "mean_time_per_case_us", "num"),
    ]
    names = list(CONFIGS)
    width = 26
    print(f"AgentOps benchmark | dataset={DATASET_VERSION} | cases={len(CASES)} | python={meta['python']}")
    print("-" * (width + 21 * len(names)))
    print(f"{'Metric':<{width}}" + "".join(f"{n:>21}" for n in names))
    for label, key, kind in rows:
        print(f"{label:<{width}}" + "".join(f"{fmt(results[n]['metrics'][key], kind):>21}" for n in names))
    print("\nDisagreements with expected outcome:")
    for n in names:
        bad = [r for r in results[n]["raw"] if r["expected"] != r["observed"]]
        detail = ", ".join(f"{r['case']} ({r['observed']})" for r in bad) or "none"
        print(f"  {n}: {detail}")
    print("\nSmall synthetic dataset; results are a development aid, not evidence of general performance.")

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps({"meta": meta, "configs": results}, indent=2, default=str))
    print(f"Raw results written to {args.json}")


if __name__ == "__main__":
    main()
