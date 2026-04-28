import pandas as pd

def compute_omega(I: pd.Series, G: pd.Series) -> pd.Series:
    """Compute Omega as structure × direction."""
    return I * G
