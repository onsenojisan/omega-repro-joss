import pandas as pd
from omega_core import compute_omega, define_ratio_event, lead_event

def test_compute_omega():
    I = pd.Series([1, 2, 3])
    G = pd.Series([4, 5, 6])
    assert compute_omega(I, G).tolist() == [4, 10, 18]

def test_event_and_lead():
    df = pd.DataFrame({"ratio_95": [1, 2, 3, 4, 5]})
    event, threshold = define_ratio_event(df, q=0.8)
    assert threshold == 4.2
    assert event.tolist() == [0, 0, 0, 0, 1]
    assert lead_event(event, lead_hours=1).tolist()[:4] == [0, 0, 0, 1]
