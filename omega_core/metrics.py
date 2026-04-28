import numpy as np
import pandas as pd

def event_rate_by_decile(
    df: pd.DataFrame,
    omega_col: str = "Omega",
    event_col: str = "event_lead",
    deciles: int = 10,
) -> pd.DataFrame:
    """Compute event rate by Omega decile."""
    tmp = df[[omega_col, event_col]].dropna().copy()
    tmp["omega_decile"] = pd.qcut(
        tmp[omega_col], deciles, labels=False, duplicates="drop"
    )
    out = (
        tmp.groupby("omega_decile")[event_col]
        .agg(["mean", "sum", "count"])
        .reset_index()
        .rename(columns={"mean": "event_rate", "sum": "event_hits", "count": "n"})
    )
    return out

def top_vs_lower_rate(
    df: pd.DataFrame,
    omega_col: str = "Omega",
    event_col: str = "event_lead",
    deciles: int = 10,
) -> pd.DataFrame:
    """Compare event rate in the highest Omega decile against lower deciles."""
    tmp = df[[omega_col, event_col]].dropna().copy()
    tmp["omega_decile"] = pd.qcut(
        tmp[omega_col], deciles, labels=False, duplicates="drop"
    )
    top_bin = tmp["omega_decile"].max()
    tmp["group"] = np.where(
        tmp["omega_decile"] == top_bin,
        "Top Omega decile",
        "Lower Omega deciles",
    )
    out = (
        tmp.groupby("group")[event_col]
        .agg(["mean", "sum", "count"])
        .reset_index()
        .rename(columns={"mean": "event_rate", "sum": "event_hits", "count": "n"})
    )
    return out
