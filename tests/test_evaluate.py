"""Unit tests for the eval harness's hit() judgement (no LLM needed)."""
import pandas as pd
from evaluate import hit


def test_hit_matches_value_in_first_row():
    df = pd.DataFrame([{"Country": "Japan", "eff": 11.58}])
    assert hit(df, "Japan")


def test_hit_is_case_insensitive():
    df = pd.DataFrame([{"Country": "Japan"}])
    assert hit(df, "japan")


def test_hit_misses_when_absent():
    df = pd.DataFrame([{"Country": "Hong Kong"}])
    assert not hit(df, "Japan")


def test_hit_handles_empty_result():
    assert not hit(pd.DataFrame(), "Japan")