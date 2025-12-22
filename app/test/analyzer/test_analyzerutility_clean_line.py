import pytest
from analyzer.AnalyzerUtility import clean_line


def test_clean_line_none_input():
    assert clean_line(None) is None


def test_clean_line_comment_only():
    assert clean_line("   # full comment   ") is None


def test_clean_line_inline_comment():
    assert (
        clean_line("allow foo bar:dir { read write }; # trailing comment")
        == "allow foo bar:dir { read write };"
    )


def test_clean_line_hash_in_single_quotes():
    assert clean_line("type 'abc#def';") == "type 'abc#def';"


def test_clean_line_hash_in_double_quotes():
    assert clean_line('message "hash # inside" # outside') == 'message "hash # inside"'


def test_clean_line_double_dash_removed():
    assert clean_line("some--value") == "somevalue"


def test_clean_line_whitespace_trimmed():
    assert clean_line("   something   ") == "something"
