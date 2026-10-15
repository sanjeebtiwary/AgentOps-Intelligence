"""Execution engine: the single controlled path from request to outcome.

Sequence (docs/architecture.md section 4):
validate -> resolve tool -> policy -> execute -> verify -> structured outcome.
A request stops at the first stage that rejects it.
"""

from __future__ import annotations

import time
from collections.abc import Mapping
from dataclasses import replace
from typing import Optional

from .models import (
    Outcome,
    Status,
    ToolArgumentError,
    ToolRequest,
    UnknownToolError,
    VerificationResult,
)
from .policy import PolicyEngine
from .registry import ToolRegistry
from .verification import Verifier


def _describe(exc: BaseException) -> str:
    return f"{type(exc).__name__}: {exc}"


class ExecutionEngine:
    def __init__(
        self,
        registry: ToolRegistry,
        policy: Optional[PolicyEngine] = None,
        verifier: Optional[Verifier] = None,
    ) -> None:
        self.registry = registry
        self.policy = policy
        self.verifier = verifier

    def execute(self, request: ToolRequest) -> Outcome:
        start = time.perf_counter()
        outcome = self._run(request)
        return replace(outcome, duration_s=time.perf_counter() - start)

    def _run(self, request: ToolRequest) -> Outcome:
        # 1. structural validation
        if not isinstance(request, ToolRequest):
            return Outcome(
                ToolRequest("<invalid>"), Status.INVALID_REQUEST, error="request must be a ToolRequest"
            )
        if not isinstance(request.tool, str) or not request.tool.strip():
            return Outcome(request, Status.INVALID_REQUEST, error="tool name must be a non-empty string")
        if not isinstance(request.args, Mapping):
            return Outcome(request, Status.INVALID_REQUEST, error="args must be a mapping")

        # 2. resolve
        try:
            tool = self.registry.resolve(request.tool)
        except UnknownToolError:
            return Outcome(request, Status.UNKNOWN_TOOL, error=f"unknown tool: {request.tool!r}")

        # 3. policy: a denial returns here and never reaches the tool
        decision = None
        if self.policy is not None:
            decision = self.policy.evaluate(request)
            if not decision.allowed:
                return Outcome(request, Status.POLICY_DENIED, error=decision.reason, policy=decision)

        # 4. execute
        try:
            result = tool.func(request.args)
        except ToolArgumentError as exc:
            return Outcome(
                request, Status.INVALID_REQUEST, error=_describe(exc), policy=decision, tool_invoked=True
            )
        except Exception as exc:  # noqa: BLE001 - tool errors must be captured, never raised
            return Outcome(
                request, Status.EXECUTION_FAILURE, error=_describe(exc), policy=decision, tool_invoked=True
            )

        # 5. verify
        verification = None
        if self.verifier is not None:
            try:
                verification = self.verifier.verify(request, result)
            except Exception as exc:  # noqa: BLE001 - a broken verifier must not pass silently
                verification = VerificationResult(False, f"verifier error: {_describe(exc)}")
            if not verification.passed:
                return Outcome(
                    request,
                    Status.VERIFICATION_FAILURE,
                    result=result,
                    error=verification.reason,
                    policy=decision,
                    verification=verification,
                    tool_invoked=True,
                )

        return Outcome(
            request,
            Status.SUCCESS,
            result=result,
            policy=decision,
            verification=verification,
            tool_invoked=True,
        )
