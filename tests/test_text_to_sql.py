"""Unit tests for cleaning the model's SQL output (no LLM needed)."""
from text_to_sql import clean_sql

GOOD = "SELECT Country FROM sales LIMIT 1"


def test_bare_sql_unchanged():
    assert clean_sql(GOOD) == GOOD


def test_strips_sql_code_fence():
    assert clean_sql(f"```sql\n{GOOD}\n```") == GOOD


def test_strips_plain_code_fence():
    assert clean_sql(f"```\n{GOOD}\n```") == GOOD


def test_strips_sql_label():
    assert clean_sql(f"SQL: {GOOD}") == GOOD


def test_strips_trailing_semicolon():
    assert clean_sql(f"{GOOD};") == GOOD


def test_strips_combined_noise():
    assert clean_sql(f"```sql\n{GOOD};\n```  ") == GOOD