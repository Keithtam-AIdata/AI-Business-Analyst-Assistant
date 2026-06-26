"""Unit tests for the SQL safety guardrail (no LLM needed)."""
import pytest
from sql_guard import validate_sql, UnsafeSQLError


def test_allows_plain_select():
    assert "SELECT" in validate_sql("SELECT Country FROM sales GROUP BY Country").upper()


def test_appends_limit_when_missing():
    assert "LIMIT" in validate_sql("SELECT Country FROM sales").upper()


def test_keeps_existing_limit_single():
    assert validate_sql("SELECT Country FROM sales LIMIT 5").upper().count("LIMIT") == 1


def test_blocks_drop():
    with pytest.raises(UnsafeSQLError):
        validate_sql("DROP TABLE sales")


def test_blocks_injection_via_second_statement():
    with pytest.raises(UnsafeSQLError):
        validate_sql("SELECT * FROM sales; DELETE FROM sales")


def test_blocks_update():
    with pytest.raises(UnsafeSQLError):
        validate_sql("UPDATE sales SET Revenue = 0")


def test_blocks_unknown_table():
    with pytest.raises(UnsafeSQLError):
        validate_sql("SELECT * FROM customers")


def test_allows_cte():
    sql = "WITH t AS (SELECT Country FROM sales) SELECT * FROM t LIMIT 1"
    assert "SELECT" in validate_sql(sql).upper()


def test_keyword_inside_string_value_is_not_blocked():
    out = validate_sql("SELECT COUNT(*) FROM sales WHERE ReturnReason = 'Changed Mind'")
    assert "SELECT" in out.upper()