# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/).

## [2.0.0] — Phase 1: text-to-SQL

### Added
- **DuckDB warehouse layer** (`db.py`) — CSV loaded into an in-process SQL
  database, with schema introspection (column types + categorical values) to
  ground the model's SQL.
- **text-to-SQL generation** (`text_to_sql.py`) — schema-aware prompting turns a
  natural-language question into a DuckDB query; output is parsed/cleaned of
  markdown wrappers.
- **SQL safety guardrails** (`sql_guard.py`) — five checks (single statement,
  read-only, no write/DDL keywords, table allowlist, enforced LIMIT).
- **Pipeline with self-correction** (`pipeline.py`) — on an execution error, the
  error is fed back to the model for one retry; safety failures are not retried.
- **Evaluation harness** (`evaluate.py`) — scores the pipeline against
  data-verified ground truth. Current accuracy: 10/10.
- **Architecture diagram** and rewritten README.

### Changed
- The assistant's Q&A now runs on text-to-SQL instead of the keyword KPI engine.
  Answers show the AI-written SQL, the query result, and the interpretation.
- Several answers became *more* accurate than the old engine (e.g. order-weighted
  return rate via `SUM(rate*orders)/SUM(orders)` instead of a flat average).

## [1.1.0] — Realistic dataset & redesign

### Added
- **Pattern-driven dataset** (`generate_data.py`) — 6,912 rows built as
  `base × business multipliers × noise`, replacing purely random data.
- Separated, unit-testable analytics layer (`analytics.py`).

### Changed
- Rebuilt the UI into a consulting-report visual style.
- KPI engine moved to a dimension × metric design.

## [1.0.0] — Initial release

### Added
- ChatGPT-style business analytics assistant: keyword KPI engine + OpenAI
  interpretation, Streamlit UI, live demo.