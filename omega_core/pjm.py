import pandas as pd
from .omega import compute_omega

REQUIRED_COLUMNS = ["datetime_beginning_ept", "pnode_name", "total_lmp_rt"]

def load_pjm_lmp(path: str) -> pd.DataFrame:
    """Load PJM RT hourly LMP CSV and normalize column names."""
    rt = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLUMNS if c not in rt.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    rt = rt[REQUIRED_COLUMNS].copy()
    rt.columns = ["datetime", "pnode", "rt_lmp"]
    rt["datetime"] = pd.to_datetime(rt["datetime"], errors="coerce")
    rt["rt_lmp"] = pd.to_numeric(rt["rt_lmp"], errors="coerce")
    rt = rt.dropna(subset=["datetime", "pnode", "rt_lmp"])
    return rt.sort_values(["datetime", "pnode"]).reset_index(drop=True)

def compute_pjm_features(rt: pd.DataFrame, min_count: int = 10) -> pd.DataFrame:
    """Compute PJM cross-sectional features and Omega."""
    rto = rt[rt["pnode"] == "PJM-RTO"][["datetime", "rt_lmp"]].copy()
    rto.columns = ["datetime", "p_rto"]

    zones = rt[rt["pnode"] != "PJM-RTO"].copy()
    zone_stats = (
        zones.groupby("datetime")["rt_lmp"]
        .agg(
            sigma_zone="std",
            p50=lambda x: x.quantile(0.50),
            p95=lambda x: x.quantile(0.95),
            count="count",
        )
        .reset_index()
    )
    zone_stats = zone_stats[zone_stats["count"] > min_count].copy()

    df = (
        zone_stats.merge(rto, on="datetime", how="inner")
        .sort_values("datetime")
        .reset_index(drop=True)
    )
    df["spread_95_rto"] = (df["p95"] - df["p_rto"]).clip(lower=0)
    df["Omega"] = compute_omega(df["sigma_zone"], df["spread_95_rto"])
    df["ratio_95"] = df["p95"] / (df["p_rto"] + 1e-9)
    return df
