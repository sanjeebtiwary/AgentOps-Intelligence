from agentops import PolicyConfig, PolicyEngine, ToolRequest


def ev(config=None, tool="add", **args):
    return PolicyEngine(config).evaluate(ToolRequest(tool, args))


def test_allows_normal_request():
    assert ev(a=1, b=2).allowed


def test_denied_tool():
    d = ev(PolicyConfig(denied_tools=frozenset({"add"})), a=1, b=2)
    assert not d.allowed and d.rule == "denied_tool"


def test_allow_list():
    cfg = PolicyConfig(allowed_tools=frozenset({"word_count"}))
    assert not ev(cfg, a=1, b=2).allowed
    assert ev(cfg, tool="word_count", text="x").allowed


def test_number_limit_boundary():
    cfg = PolicyConfig(max_abs_number=100)
    assert ev(cfg, a=100, b=-100).allowed
    d = ev(cfg, a=101, b=1)
    assert not d.allowed and d.rule == "number_too_large"
    assert not ev(cfg, a=1, b=-101).allowed


def test_non_finite_and_bool_handling():
    assert ev(a=float("nan"), b=1).rule == "non_finite_number"
    assert ev(a=True, b=1).allowed  # bools are not numbers; the tool rejects them


def test_text_limit_boundary():
    cfg = PolicyConfig(max_text_length=5)
    assert ev(cfg, tool="word_count", text="x" * 5).allowed
    assert ev(cfg, tool="word_count", text="x" * 6).rule == "text_too_long"


def test_arg_count():
    assert ev(PolicyConfig(max_args=1), a=1, b=2).rule == "too_many_args"
