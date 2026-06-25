"""
sql_guard.py
============
Validate LLM-generated SQL before it ever touches the database (Phase 1, Step 3).

The model is helpful but not trusted. Every query it writes passes through here
first. This is the line between "naively running whatever the AI produced" and
"validating, then executing" — the difference a senior reviewer looks for.

Five checks:
  1. single statement      — block injection via a second ';'-separated statement
  2. read-only             — must start with SELECT / WITH
  3. no write/DDL keywords — defense-in-depth against DROP/DELETE/UPDATE/ATTACH/...
  4. table allowlist       — only the 'sales' table (CTE names are allowed too)
  5. row cap               — append LIMIT if the query has none
"""

import re

ALLOWED_TABLES = {"sales"}
DEFAULT_LIMIT = 1000

# Write / DDL / DuckDB-specific dangerous operations that never appear in a
# legitimate analytical SELECT.
WRITE_KEYWORDS = re.compile(
    r"\b(drop|delete|update|insert|alter|create|attach|detach|copy|pragma|"
    r"truncate|replace|install|load|export|vacuum)\b", re.I)


class UnsafeSQLError(Exception):
    """Raised when a query fails a guardrail check."""


def _strip_string_literals(sql: str) -> str:
    """Replace '...' literals with '' so their contents can't trip keyword/table
    checks (e.g. a value like 'changed mind' shouldn't look like a keyword)."""
    return re.sub(r"'[^']*'", "''", sql)


def validate_sql(sql: str, allowed_tables=ALLOWED_TABLES, default_limit=DEFAULT_LIMIT) -> str:
    """Return a safe, executable SQL string, or raise UnsafeSQLError.

    On success the returned string may have a LIMIT appended.
    """
    s = sql.strip().rstrip(";").strip()
    if not s:
        raise UnsafeSQLError("empty query")

    # 1. single statement
    if ";" in s:
        raise UnsafeSQLError("multiple statements are not allowed")

    probe = _strip_string_literals(s)  # check against a literal-free copy

    # 2. read-only
    if not re.match(r"(?is)^\s*(select|with)\b", probe):
        raise UnsafeSQLError("only SELECT / WITH queries are allowed")

    # 3. no write / DDL keywords
    hit = WRITE_KEYWORDS.search(probe)
    if hit:
        raise UnsafeSQLError(f"forbidden keyword: {hit.group(0).upper()}")

    # 4. table allowlist (CTE names defined via 'name AS (' are permitted)
    cte_names = {m.lower() for m in re.findall(r"\b([a-zA-Z_]\w*)\s+as\s*\(", probe, re.I)}
    referenced = {m.lower() for m in re.findall(r"\b(?:from|join)\s+([a-zA-Z_]\w*)", probe, re.I)}
    unknown = referenced - {t.lower() for t in allowed_tables} - cte_names
    if unknown:
        raise UnsafeSQLError(f"unknown table(s): {', '.join(sorted(unknown))}")

    # 5. enforce a row cap
    if not re.search(r"\blimit\b", probe, re.I):
        s += f" LIMIT {default_limit}"

    return s


if __name__ == "__main__":
    tests = [
        "SELECT Country, SUM(Revenue) r FROM sales GROUP BY Country ORDER BY r DESC LIMIT 1",
        "SELECT ProductCategory, AVG(ReturnRate) FROM sales GROUP BY ProductCategory",  # no LIMIT
        "DROP TABLE sales",
        "SELECT * FROM sales; DELETE FROM sales",
        "UPDATE sales SET Revenue = 0",
        "SELECT * FROM customers",
        "WITH t AS (SELECT Country, SUM(Revenue) r FROM sales GROUP BY Country) SELECT * FROM t ORDER BY r DESC LIMIT 1",
        "SELECT COUNT(*) FROM sales WHERE ReturnReason = 'Changed Mind'",
    ]
    for t in tests:
        try:
            print(f"[PASS] {validate_sql(t)[:70]}")
        except UnsafeSQLError as e:
            print(f"[BLOCK] {e}  <- {t[:45]}")