"""Deterministic utility tools.

Every tool takes a mapping of named arguments, validates them strictly and
raises ``ToolArgumentError`` on bad input. Booleans are rejected as numbers.
"""

from __future__ import annotations

import math
from typing import Any, Mapping

from .models import ToolArgumentError
from .registry import Tool, ToolRegistry


def _exact_args(args: Mapping[str, Any], names: tuple[str, ...]) -> None:
    if not isinstance(args, Mapping):
        raise ToolArgumentError("arguments must be a mapping")
    missing = [n for n in names if n not in args]
    extra = [n for n in args if n not in names]
    if missing:
        raise ToolArgumentError(f"missing argument(s): {', '.join(missing)}")
    if extra:
        raise ToolArgumentError(f"unexpected argument(s): {', '.join(map(str, extra))}")


def _number(args: Mapping[str, Any], name: str) -> int | float:
    value = args[name]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ToolArgumentError(f"{name!r} must be a number")
    if isinstance(value, float) and not math.isfinite(value):
        raise ToolArgumentError(f"{name!r} must be finite")
    return value


def _text(args: Mapping[str, Any], name: str) -> str:
    value = args[name]
    if not isinstance(value, str):
        raise ToolArgumentError(f"{name!r} must be a string")
    return value


def add(args: Mapping[str, Any]) -> int | float:
    _exact_args(args, ("a", "b"))
    return _number(args, "a") + _number(args, "b")


def multiply(args: Mapping[str, Any]) -> int | float:
    _exact_args(args, ("a", "b"))
    return _number(args, "a") * _number(args, "b")


def divide(args: Mapping[str, Any]) -> float:
    _exact_args(args, ("a", "b"))
    a, b = _number(args, "a"), _number(args, "b")
    return a / b  # ZeroDivisionError is an execution failure, not an argument error


def normalize_text(args: Mapping[str, Any]) -> str:
    """Lower-case and collapse all whitespace runs to single spaces."""
    _exact_args(args, ("text",))
    return " ".join(_text(args, "text").split()).lower()


def word_count(args: Mapping[str, Any]) -> int:
    _exact_args(args, ("text",))
    return len(_text(args, "text").split())


def build_default_registry() -> ToolRegistry:
    return ToolRegistry(
        [
            Tool("add", add, "Add two numbers (a, b)"),
            Tool("multiply", multiply, "Multiply two numbers (a, b)"),
            Tool("divide", divide, "Divide a by b"),
            Tool("normalize_text", normalize_text, "Lower-case and collapse whitespace (text)"),
            Tool("word_count", word_count, "Count whitespace-separated words (text)"),
        ]
    )
