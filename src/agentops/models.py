"""Core data structures shared by every component."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Optional


class _NotSet:
    """Sentinel meaning 'no value supplied' (distinct from None)."""

    def __repr__(self) -> str:
        return "NOT_SET"

    def __bool__(self) -> bool:
        return False


NOT_SET: Any = _NotSet()


class ToolArgumentError(ValueError):
    """Raised by a tool when its arguments are invalid."""


class UnknownToolError(KeyError):
    """Raised by the registry when a tool name is not registered."""


class Status(str, Enum):
    """Mutually exclusive final status of one request.

    Matches the failure categories in docs/architecture.md. Each request
    gets exactly one status, so overlapping categories are never double
    counted: the *first* stage that stops the request decides the status.
    """

    SUCCESS = "success"
    INVALID_REQUEST = "invalid_request"
    UNKNOWN_TOOL = "unknown_tool"
    POLICY_DENIED = "policy_denied"
    EXECUTION_FAILURE = "execution_failure"
    VERIFICATION_FAILURE = "verification_failure"


@dataclass(frozen=True)
class ToolRequest:
    """A request to run one tool.

    ``expected`` optionally carries a task-specific expected result which
    the verifier checks in addition to the tool's own postcondition.
    """

    tool: str
    args: Mapping[str, Any] = field(default_factory=dict)
    expected: Any = NOT_SET


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    rule: Optional[str] = None
    reason: Optional[str] = None

    @classmethod
    def allow(cls) -> "PolicyDecision":
        return cls(True)

    @classmethod
    def deny(cls, rule: str, reason: str) -> "PolicyDecision":
        return cls(False, rule, reason)


@dataclass(frozen=True)
class VerificationResult:
    passed: bool
    reason: Optional[str] = None


@dataclass(frozen=True)
class Outcome:
    """Structured result of ``ExecutionEngine.execute``."""

    request: ToolRequest
    status: Status
    result: Any = None  # present for SUCCESS; kept for inspection on VERIFICATION_FAILURE
    error: Optional[str] = None
    policy: Optional[PolicyDecision] = None
    verification: Optional[VerificationResult] = None
    tool_invoked: bool = False  # True iff the tool implementation was called
    duration_s: float = 0.0

    @property
    def ok(self) -> bool:
        return self.status is Status.SUCCESS

    @property
    def verified(self) -> Optional[bool]:
        """True/False if verification ran, None if it did not."""
        return None if self.verification is None else self.verification.passed
