"""
analytics.py
============
Dashboard data layer: loads the dataset and builds the aggregations the
Streamlit charts and tables display.

No Streamlit, no OpenAI — pure Pandas, so it stays easy to reason about and test.
(The natural-language Q&A is handled separately by the text-to-SQL pipeline in
db.py / text_to_sql.py / sql_guard.py / pipeline.py.)
"""

from __future__ import annotations
import pandas as pd

DATA_PATH = "data/business_data.csv"


def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    """Read the CSV and add a real monthly period for correct time ordering."""
    df = pd.read_csv(path)
    df["MonthPeriod"] = pd.PeriodIndex(df["Month"], freq="M")
    return df


def build_aggregations(df: pd.DataFrame) -> dict:
    """Pre-compute the by-dimension tables, the monthly trend, and the headline
    figures used across the dashboard."""

    def by(dim: str) -> pd.DataFrame:
        g = (df.groupby(dim)
               .agg(Revenue=("Revenue", "sum"),
                    Orders=("Orders", "sum"),
                    MarketingSpend=("MarketingSpend", "sum"),
                    NetProfit=("NetProfit", "sum"),
                    GrossMarginPct=("GrossMarginPct", "mean"),
                    ReturnRate=("ReturnRate", "mean"),
                    ConversionRate=("ConversionRate", "mean"),
                    AverageOrderValue=("AverageOrderValue", "mean"),
                    CustomerSatisfaction=("CustomerSatisfaction", "mean"))
               .reset_index())
        g["RevenuePerMarketingDollar"] = (g["Revenue"] / g["MarketingSpend"]).round(2)
        g["NetMarginPct"] = g["NetProfit"] / g["Revenue"]
        return g

    country = by("Country")
    category = by("ProductCategory")
    channel = by("Channel")
    segment = by("CustomerSegment")

    monthly = (df.groupby("MonthPeriod")
                 .agg(Revenue=("Revenue", "sum"), NetProfit=("NetProfit", "sum"))
                 .reset_index())
    monthly["Month"] = monthly["MonthPeriod"].astype(str)

    headline = {
        "total_revenue": df["Revenue"].sum(),
        "total_orders": df["Orders"].sum(),
        "total_net_profit": df["NetProfit"].sum(),
        "net_margin": df["NetProfit"].sum() / df["Revenue"].sum(),
        "top_country": country.sort_values("Revenue", ascending=False).iloc[0]["Country"],
        "best_efficiency_country": country.sort_values("RevenuePerMarketingDollar", ascending=False).iloc[0]["Country"],
        "lowest_sat_country": country.sort_values("CustomerSatisfaction").iloc[0]["Country"],
        "top_category": category.sort_values("Revenue", ascending=False).iloc[0]["ProductCategory"],
        "most_profitable_category": category.sort_values("NetProfit", ascending=False).iloc[0]["ProductCategory"],
        "highest_return_category": category.sort_values("ReturnRate", ascending=False).iloc[0]["ProductCategory"],
        "n_countries": df["Country"].nunique(),
        "n_channels": df["Channel"].nunique(),
        "n_segments": df["CustomerSegment"].nunique(),
        "n_categories": df["ProductCategory"].nunique(),
        "n_months": df["Month"].nunique(),
    }
    return {"country": country, "category": category, "channel": channel,
            "segment": segment, "monthly": monthly, "headline": headline}