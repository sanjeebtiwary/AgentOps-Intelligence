import pytest

from agentops import Tool, ToolArgumentError, ToolRegistry, UnknownToolError, tools


def test_arithmetic_tools():
    assert tools.add({"a": 2, "b": 3}) == 5
    assert tools.multiply({"a": 4, "b": 2.5}) == 10
    assert tools.divide({"a": 10, "b": 4}) == 2.5


def test_divide_by_zero_is_not_an_argument_error():
    with pytest.raises(ZeroDivisionError):
        tools.divide({"a": 1, "b": 0})


@pytest.mark.parametrize(
    "args",
    [
        {"a": 1},
        {"a": 1, "b": 2, "c": 3},
        {"a": "1", "b": 2},
        {"a": True, "b": 2},
        {"a": float("nan"), "b": 1},
        {"a": float("inf"), "b": 1},
    ],
)
def test_invalid_numeric_args(args):
    with pytest.raises(ToolArgumentError):
        tools.add(args)


def test_text_tools():
    assert tools.normalize_text({"text": "  Hello \n WORLD "}) == "hello world"
    assert tools.word_count({"text": "a  b\tc\n"}) == 3
    assert tools.word_count({"text": ""}) == 0
    with pytest.raises(ToolArgumentError):
        tools.word_count({"text": 5})


def test_registry_register_resolve_duplicates():
    reg = ToolRegistry()
    reg.register(Tool("t", lambda a: 1))
    assert "t" in reg and reg.names() == ["t"]
    assert reg.resolve("t").func({}) == 1
    with pytest.raises(ValueError):
        reg.register(Tool("t", lambda a: 2))
    reg.register(Tool("t", lambda a: 2), replace=True)
    assert reg.resolve("t").func({}) == 2
    with pytest.raises(UnknownToolError):
        reg.resolve("nope")
    with pytest.raises(ValueError):
        reg.register(Tool("  ", lambda a: 1))
