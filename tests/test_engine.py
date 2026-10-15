import pytest

from agentops import (
    ExecutionEngine,
    PolicyConfig,
    PolicyEngine,
    Status,
    Tool,
    ToolRegistry,
    ToolRequest,
    VerificationResult,
    Verifier,
    build_default_registry,
)


def test_success_with_verification(full_engine):
    o = full_engine.execute(ToolRequest("add", {"a": 2, "b": 3}))
    assert o.status is Status.SUCCESS and o.ok and o.result == 5
    assert o.verified is True and o.policy.allowed and o.tool_invoked
    assert o.duration_s >= 0


def test_success_without_policy_or_verifier_is_unverified(registry):
    o = ExecutionEngine(registry).execute(ToolRequest("add", {"a": 1, "b": 1}))
    assert o.ok and o.verified is None and o.policy is None


def test_unknown_tool(full_engine):
    o = full_engine.execute(ToolRequest("rm_rf", {}))
    assert o.status is Status.UNKNOWN_TOOL and not o.tool_invoked


@pytest.mark.parametrize(
    "bad", [None, "add", ToolRequest("", {}), ToolRequest("add", [1, 2]), ToolRequest(None, {})]
)
def test_malformed_requests_are_invalid(full_engine, bad):
    o = full_engine.execute(bad)
    assert o.status is Status.INVALID_REQUEST and not o.tool_invoked


def test_bad_arguments_are_invalid_request(full_engine):
    o = full_engine.execute(ToolRequest("add", {"a": "x", "b": 1}))
    assert o.status is Status.INVALID_REQUEST and o.tool_invoked


def test_tool_exception_is_execution_failure(full_engine):
    o = full_engine.execute(ToolRequest("divide", {"a": 1, "b": 0}))
    assert o.status is Status.EXECUTION_FAILURE and "ZeroDivisionError" in o.error
    assert not o.ok and o.verification is None


def test_denied_action_never_reaches_tool(spy_registry):
    engine = ExecutionEngine(spy_registry, PolicyEngine(PolicyConfig(denied_tools=frozenset({"spy"}))))
    o = engine.execute(ToolRequest("spy", {}))
    assert o.status is Status.POLICY_DENIED and not o.tool_invoked
    assert o.policy.rule == "denied_tool"
    assert spy_registry.calls == []


def test_allowed_action_reaches_tool(spy_registry):
    ExecutionEngine(spy_registry, PolicyEngine()).execute(ToolRequest("spy", {"k": 1}))
    assert spy_registry.calls == [{"k": 1}]


def test_policy_denial_is_not_execution_failure(full_engine):
    o = full_engine.execute(ToolRequest("add", {"a": 10**12, "b": 1}))
    assert o.status is Status.POLICY_DENIED


def test_verification_failure_is_not_success():
    reg = ToolRegistry([Tool("bad_add", lambda a: a["a"] + a["b"] + 1)])
    v = Verifier({"bad_add": lambda args, r: VerificationResult(r == args["a"] + args["b"], "off by one")})
    o = ExecutionEngine(reg, verifier=v).execute(ToolRequest("bad_add", {"a": 1, "b": 1}))
    assert o.status is Status.VERIFICATION_FAILURE and not o.ok
    assert o.verified is False and o.result == 3 and o.error == "off by one"


def test_crashing_verifier_does_not_pass_silently(registry):
    def boom(args, result):
        raise RuntimeError("kaput")

    o = ExecutionEngine(registry, verifier=Verifier({"add": boom})).execute(
        ToolRequest("add", {"a": 1, "b": 1})
    )
    assert o.status is Status.VERIFICATION_FAILURE and "verifier error" in o.error


def test_task_specific_expectation(full_engine):
    assert full_engine.execute(ToolRequest("add", {"a": 1, "b": 1}, expected=2)).ok
    assert (
        full_engine.execute(ToolRequest("add", {"a": 1, "b": 1}, expected=3)).status
        is Status.VERIFICATION_FAILURE
    )


def test_tool_without_postcondition_is_not_verified_success():
    reg = build_default_registry()
    reg.register(Tool("custom", lambda a: 1))
    o = ExecutionEngine(reg, verifier=Verifier()).execute(ToolRequest("custom", {}))
    assert o.status is Status.VERIFICATION_FAILURE
