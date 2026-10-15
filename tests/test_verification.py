from agentops import ToolRequest, Verifier, default_verifier
from agentops.verification import matches

V = default_verifier()


def check(tool, args, result, **kw):
    return V.verify(ToolRequest(tool, args, **kw), result)


def test_correct_results_pass():
    assert check("add", {"a": 0.1, "b": 0.2}, 0.1 + 0.2).passed
    assert check("divide", {"a": 1, "b": 3}, 1 / 3).passed
    assert check("normalize_text", {"text": " A  B "}, "a b").passed
    assert check("word_count", {"text": "a b c"}, 3).passed


def test_incorrect_results_fail():
    assert not check("add", {"a": 1, "b": 2}, 4).passed
    assert not check("multiply", {"a": 2, "b": 3}, 5).passed
    assert not check("word_count", {"text": "a b"}, 3).passed
    assert not check("normalize_text", {"text": "A B"}, "A B").passed
    assert not check("normalize_text", {"text": "a b"}, "a  b").passed
    assert not check("normalize_text", {"text": "a b"}, "a c").passed


def test_malformed_and_missing_results_fail():
    assert not check("add", {"a": 1, "b": 2}, None).passed
    assert not check("add", {"a": 1, "b": 2}, "3").passed
    assert not check("add", {"a": 1, "b": 2}, True).passed
    assert not check("word_count", {"text": "a"}, -1).passed
    assert not check("word_count", {"text": "a"}, 1.0).passed
    assert not check("normalize_text", {"text": "a"}, 5).passed


def test_boundary_large_ints_are_exact():
    big = 10**30
    assert check("add", {"a": big, "b": 1}, big + 1).passed
    assert not check("add", {"a": big, "b": 1}, big).passed


def test_expected_value_is_checked_in_addition():
    assert check("add", {"a": 1, "b": 2}, 3, expected=3).passed
    r = check("add", {"a": 1, "b": 2}, 3, expected=4)
    assert not r.passed and "expected 4" in r.reason


def test_fails_closed_without_postcondition():
    assert not Verifier().verify(ToolRequest("x"), 1).passed
    assert Verifier(require_postcondition=False).verify(ToolRequest("x"), 1).passed


def test_matches_type_strictness():
    assert not matches("1", 1)
    assert matches(1.0, 1)
