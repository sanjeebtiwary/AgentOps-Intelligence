"""Independent outcome verification.

A postcondition inspects (arguments, result) and decides whether the result
satisfies explicit expectations. It only detects what it checks: passing is
not proof of general correctness.
"""

from __future__ import annotations

import math
from typing import Any, Callable, Mapping

from .models import NOT_SET, ToolRequest, VerificationResult

Postcondition = Callable[[Mapping[str, Any], Any], VerificationResult]

_OK = VerificationResult(True)


def _fail(reason: str) -> VerificationResult:
    return VerificationResult(False, reason)


def _is_number(x: Any) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def matches(actual: Any, expected: Any) -> bool:
    """Exact for ints/strings, tolerant (1e-9 relative) for floats."""
    if _is_number(actual) and _is_number(expected):
        if isinstance(actual, int) and isinstance(expected, int):
            return actual == expected
        try:
            return math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-12)
        except OverflowError:
            return actual == expected
    return type(actual) is type(expected) and actual == expected


# -- postconditions ------------------------------------------------------
def _arith(op: Callable[[Any, Any], Any]) -> Postcondition:
    def check(args: Mapping[str, Any], result: Any) -> VerificationResult:
        if not _is_number(result):
            return _fail(f"result is not a number: {result!r}")
        expected = op(args["a"], args["b"])
        if not matches(result, expected):
            return _fail(f"expected {expected!r}, got {result!r}")
        return _OK

    return check


add_postcondition = _arith(lambda a, b: a + b)
multiply_postcondition = _arith(lambda a, b: a * b)
divide_postcondition = _arith(lambda a, b: a / b)


def normalize_text_postcondition(args: Mapping[str, Any], result: Any) -> VerificationResult:
    if not isinstance(result, str):
        return _fail(f"result is not a string: {result!r}")
    if result != result.lower():
        return _fail("result contains upper-case characters")
    if result != " ".join(result.split()):
        return _fail("result has leading, trailing or repeated whitespace")
    if result.split() != args["text"].lower().split():
        return _fail("result does not preserve the words of the input")
    return _OK


def word_count_postcondition(args: Mapping[str, Any], result: Any) -> VerificationResult:
    if not isinstance(result, int) or isinstance(result, bool) or result < 0:
        return _fail(f"result is not a non-negative integer: {result!r}")
    expected = len(args["text"].split())
    return _OK if result == expected else _fail(f"expected {expected}, got {result}")


class Verifier:
    """Maps tool names to postconditions and applies them.

    ``require_postcondition=True`` (default) fails closed: a tool with no
    registered postcondition cannot be reported as verified.
    """

    def __init__(
        self, postconditions: Mapping[str, Postcondition] | None = None, *, require_postcondition: bool = True
    ) -> None:
        self._postconditions: dict[str, Postcondition] = dict(postconditions or {})
        self.require_postcondition = require_postcondition

    def register(self, tool_name: str, postcondition: Postcondition) -> None:
        self._postconditions[tool_name] = postcondition

    def verify(self, request: ToolRequest, result: Any) -> VerificationResult:
        check = self._postconditions.get(request.tool)
        if check is None:
            if self.require_postcondition:
                return _fail(f"no postcondition registered for {request.tool!r}")
        else:
            outcome = check(request.args, result)
            if not outcome.passed:
                return outcome
        if request.expected is not NOT_SET and not matches(result, request.expected):
            return _fail(f"expected {request.expected!r}, got {result!r}")
        return _OK


def default_verifier() -> Verifier:
    return Verifier(
        {
            "add": add_postcondition,
            "multiply": multiply_postcondition,
            "divide": divide_postcondition,
            "normalize_text": normalize_text_postcondition,
            "word_count": word_count_postcondition,
        }
    )
