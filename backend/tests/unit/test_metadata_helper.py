from app.helpers.metadata import get_book_category, build_chunk_metadata


def test_category_cashflow_finance():
    assert get_book_category("Profit First by Mike Michalowicz") == "cashflow_finance"


def test_category_lead_generation():
    assert get_book_category("100M Leads by Alex Hormozi") == "lead_generation"


def test_category_scaling():
    assert get_book_category("Good to Great by Jim Collins") == "scaling"


def test_category_business_systems():
    assert get_book_category("Traction Get A Grip On Your Business") == "business_systems"


def test_category_strategy_power():
    assert get_book_category("48 Laws of Power by Robert Greene") == "strategy_power"


def test_category_psychology():
    assert get_book_category("Scattered Minds by Gabor Maté") == "psychology"


def test_category_unknown_returns_general():
    assert get_book_category("Unknown Book Title XYZ 9999") == "general"


def test_build_chunk_metadata_has_all_keys():
    meta = build_chunk_metadata("Profit First", "Mike Michalowicz", "cashflow_finance", "Chapter 1", "child")
    assert {"book_title", "author", "category", "chapter", "chunk_level"} <= meta.keys()


def test_build_chunk_metadata_none_chapter_becomes_empty_string():
    meta = build_chunk_metadata("Profit First", "Mike Michalowicz", "cashflow_finance", None, "parent")
    assert meta["chapter"] == ""
