from app.helpers.text import (
    clean_text,
    count_tokens,
    truncate_to_token_limit,
    split_into_sentences,
)


def test_clean_text_removes_lone_page_numbers():
    raw = "Some paragraph text.\n\n42\n\nNext paragraph."
    result = clean_text(raw)
    assert "\n42\n" not in result


def test_clean_text_collapses_excess_spaces():
    assert clean_text("hello   world") == "hello world"


def test_clean_text_collapses_excess_newlines():
    result = clean_text("line1\n\n\n\nline2")
    assert "\n\n\n" not in result


def test_count_tokens_returns_positive_int():
    assert count_tokens("hello world") > 0


def test_count_tokens_longer_text_has_more_tokens():
    assert count_tokens("hi") < count_tokens("This is a much longer sentence with many words.")


def test_truncate_stays_within_limit():
    long_text = "Word " * 500
    result = truncate_to_token_limit(long_text, max_tokens=50)
    assert count_tokens(result) <= 50


def test_truncate_returns_full_text_if_within_limit():
    text = "Short text."
    assert truncate_to_token_limit(text, max_tokens=1000) == text


def test_split_into_sentences_splits_correctly():
    text = "First sentence. Second sentence. Third sentence."
    assert len(split_into_sentences(text)) == 3


def test_split_into_sentences_filters_empty_strings():
    assert split_into_sentences("   ") == []
