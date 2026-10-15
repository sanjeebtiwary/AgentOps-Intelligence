import pytest

from agentops import (
    ExecutionEngine,
    PolicyEngine,
    Tool,
    ToolRegistry,
    build_default_registry,
    default_verifier,
)


@pytest.fixture
def registry():
    return build_default_registry()


@pytest.fixture
def full_engine(registry):
    return ExecutionEngine(registry, PolicyEngine(), default_verifier())


@pytest.fixture
def spy_registry():
    """Registry with a tool that records every call, to prove non-execution."""
    calls = []

    def spy(args):
        calls.append(dict(args))
        return 1

    reg = ToolRegistry([Tool("spy", spy)])
    reg.calls = calls
    return reg
