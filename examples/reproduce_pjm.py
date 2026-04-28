import sys
from omega_core import (
    load_pjm_lmp,
    compute_pjm_features,
    define_ratio_event,
    lead_event,
    event_rate_by_decile,
    top_vs_lower_rate,
)

csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/rt_hrl_lmps.csv"

df = compute_pjm_features(load_pjm_lmp(csv_path), min_count=10)
df["event"], threshold = define_ratio_event(df, q=0.998)
df["event_lead"] = lead_event(df["event"], lead_hours=6)
df = df.dropna(subset=["event_lead"]).copy()
df["event_lead"] = df["event_lead"].astype(int)

print("threshold for event =", threshold)
print("event count =", int(df["event"].sum()))
print("\nEvent rate by Omega decile:")
print(event_rate_by_decile(df))
print("\nTop vs lower Omega deciles:")
print(top_vs_lower_rate(df))
