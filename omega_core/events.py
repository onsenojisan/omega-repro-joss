import pandas as pd

def define_ratio_event(df: pd.DataFrame, ratio_col: str = "ratio_95", q: float = 0.998):
    """Define event independently of Omega using an extreme ratio threshold."""
    threshold = df[ratio_col].quantile(q)
    event = (df[ratio_col] >= threshold).astype(int)
    return event, threshold

def lead_event(event: pd.Series, lead_hours: int = 6) -> pd.Series:
    """Align current Omega with a future event."""
    return event.shift(-lead_hours)
