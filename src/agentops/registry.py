"""Tool registry: the only way the engine resolves tool implementations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Mapping

from .models import UnknownToolError


@dataclass(frozen=True)
class Tool:
    name: str
    func: Callable[[Mapping[str, Any]], Any]
    description: str = ""


class ToolRegistry:
    def __init__(self, tools: Iterable[Tool] = ()) -> None:
        self._tools: dict[str, Tool] = {}
        for tool in tools:
            self.register(tool)

    def register(self, tool: Tool, *, replace: bool = False) -> None:
        if not isinstance(tool.name, str) or not tool.name.strip():
            raise ValueError("tool name must be a non-empty string")
        if tool.name in self._tools and not replace:
            raise ValueError(f"tool already registered: {tool.name!r}")
        self._tools[tool.name] = tool

    def resolve(self, name: str) -> Tool:
        try:
            return self._tools[name]
        except (KeyError, TypeError):
            raise UnknownToolError(name) from None

    def names(self) -> list[str]:
        return sorted(self._tools)

    def __contains__(self, name: object) -> bool:
        return name in self._tools
