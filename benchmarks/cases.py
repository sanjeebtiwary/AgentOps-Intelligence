"""Synthetic benchmark dataset (version 1).

Ground truth per case:
  expected_status  - the status a *correct* system should report
  truth            - the correct result value, if the operation has one
  policy_violating - True if executing the request would violate the
                     benchmark's policy (so it should be denied)

`lossy_add` is a deliberately buggy tool (it rounds its result to an int) used
only here, to give the verifier something real to catch.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from agentops import NOT_SET, Status, Tool, ToolRequest, build_default_registry
from agentops.verification import add_postcondition

DATASET_VERSION = "synthetic-v1"


@dataclass(frozen=True)
class BenchmarkCase:
    id: str
    description: str
    request: ToolRequest
    expected_status: Status
    truth: Any = NOT_SET
    policy_violating: bool = False


def benchmark_registry():
    reg = build_default_registry()
    reg.register(Tool("lossy_add", lambda a: round(a["a"] + a["b"]), "BUGGY: rounds the sum"))
    return reg


def register_benchmark_postconditions(verifier) -> None:
    verifier.register("lossy_add", add_postcondition)


S = Status
CASES: list[BenchmarkCase] = [
    BenchmarkCase("add_basic", "valid addition", ToolRequest("add", {"a": 2, "b": 3}), S.SUCCESS, 5),
    BenchmarkCase(
        "multiply_basic", "valid multiplication", ToolRequest("multiply", {"a": 4, "b": 5}), S.SUCCESS, 20
    ),
    BenchmarkCase("divide_basic", "valid division", ToolRequest("divide", {"a": 10, "b": 4}), S.SUCCESS, 2.5),
    BenchmarkCase(
        "normalize_basic",
        "valid normalization",
        ToolRequest("normalize_text", {"text": "  Hello   WORLD "}),
        S.SUCCESS,
        "hello world",
    ),
    BenchmarkCase(
        "word_count_basic",
        "valid word count",
        ToolRequest("word_count", {"text": "the quick brown fox"}),
        S.SUCCESS,
        4,
    ),
    BenchmarkCase(
        "add_float_boundary",
        "float rounding must not trip the verifier",
        ToolRequest("add", {"a": 0.1, "b": 0.2}),
        S.SUCCESS,
        0.1 + 0.2,
    ),
    BenchmarkCase(
        "divide_by_zero",
        "tool raises during execution",
        ToolRequest("divide", {"a": 1, "b": 0}),
        S.EXECUTION_FAILURE,
    ),
    BenchmarkCase(
        "add_wrong_type", "invalid argument type", ToolRequest("add", {"a": "x", "b": 1}), S.INVALID_REQUEST
    ),
    BenchmarkCase("empty_tool_name", "malformed request", ToolRequest("", {}), S.INVALID_REQUEST),
    BenchmarkCase("unknown_tool", "tool is not registered", ToolRequest("delete_all", {}), S.UNKNOWN_TOOL),
    BenchmarkCase(
        "add_over_limit",
        "numeric argument beyond policy limit (result would be correct)",
        ToolRequest("add", {"a": 10**12, "b": 1}),
        S.POLICY_DENIED,
        10**12 + 1,
        policy_violating=True,
    ),
    BenchmarkCase(
        "text_over_limit",
        "text argument beyond policy limit (result would be correct)",
        ToolRequest("normalize_text", {"text": "x" * 20_000}),
        S.POLICY_DENIED,
        "x" * 20_000,
        policy_violating=True,
    ),
    BenchmarkCase(
        "lossy_add_float",
        "buggy tool returns a wrong result",
        ToolRequest("lossy_add", {"a": 1.5, "b": 2.25}),
        S.VERIFICATION_FAILURE,
        3.75,
    ),
    BenchmarkCase(
        "lossy_add_int",
        "buggy tool happens to be right on ints",
        ToolRequest("lossy_add", {"a": 2, "b": 3}),
        S.SUCCESS,
        5,
    ),
]
