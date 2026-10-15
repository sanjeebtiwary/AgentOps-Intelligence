"""Policy enforcement: decides whether a request may run, before it runs."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Optional

from .models import PolicyDecision, ToolRequest


@dataclass(frozen=True)
class PolicyConfig:
    """Declarative policy. Defaults are deliberately restrictive."""

    allowed_tools: Optional[frozenset[str]] = None  # None = any registered tool
    denied_tools: frozenset[str] = frozenset()
    max_args: int = 8
    max_abs_number: float = 1e9
    max_text_length: int = 10_000


Rule = Callable[[ToolRequest], Optional[PolicyDecision]]


class PolicyEngine:
    """Evaluates rules in a fixed order; the first denial wins.

    Only top-level argument values are inspected. Nested structures are
    not supported by the current tools and are not examined.
    """

    def __init__(self, config: PolicyConfig | None = None) -> None:
        self.config = config or PolicyConfig()
        self._rules: list[Rule] = [
            self._denied_tool,
            self._allowed_tool,
            self._arg_count,
            self._numeric_limits,
            self._text_limits,
        ]

    def evaluate(self, request: ToolRequest) -> PolicyDecision:
        for rule in self._rules:
            decision = rule(request)
            if decision is not None and not decision.allowed:
                return decision
        return PolicyDecision.allow()

    # -- rules: return a deny decision or None ---------------------------
    def _denied_tool(self, r: ToolRequest) -> Optional[PolicyDecision]:
        if r.tool in self.config.denied_tools:
            return PolicyDecision.deny("denied_tool", f"tool {r.tool!r} is denied")
        return None

    def _allowed_tool(self, r: ToolRequest) -> Optional[PolicyDecision]:
        allowed = self.config.allowed_tools
        if allowed is not None and r.tool not in allowed:
            return PolicyDecision.deny("tool_not_allowed", f"tool {r.tool!r} is not on the allow-list")
        return None

    def _arg_count(self, r: ToolRequest) -> Optional[PolicyDecision]:
        if len(r.args) > self.config.max_args:
            return PolicyDecision.deny("too_many_args", f"more than {self.config.max_args} arguments")
        return None

    def _numeric_limits(self, r: ToolRequest) -> Optional[PolicyDecision]:
        for name, value in r.args.items():
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                continue
            if isinstance(value, float) and not math.isfinite(value):
                return PolicyDecision.deny("non_finite_number", f"argument {name!r} is not finite")
            if abs(value) > self.config.max_abs_number:
                return PolicyDecision.deny(
                    "number_too_large", f"argument {name!r} exceeds {self.config.max_abs_number:g}"
                )
        return None

    def _text_limits(self, r: ToolRequest) -> Optional[PolicyDecision]:
        for name, value in r.args.items():
            if isinstance(value, str) and len(value) > self.config.max_text_length:
                return PolicyDecision.deny(
                    "text_too_long", f"argument {name!r} exceeds {self.config.max_text_length} characters"
                )
        return None
