# omega-repro

A minimal reproducible pipeline for testing whether collapse-related events concentrate in high-Ω regimes.

This is not a prediction model. It tests structural concentration using fixed definitions.

## Main reproduction

The reference reproduction uses PJM RT hourly LMP data.

Definitions:

```text
Ω = σ_zone × max(p95 − p_RTO, 0)
event = 1 if (p95 / p_RTO) >= q(0.998)
event_lead = event shifted by 6 hours
```

## Install

```bash
pip install -e .
```

## Run

Place `rt_hrl_lmps.csv` in `data/`, then run:

```bash
python examples/reproduce_pjm.py data/rt_hrl_lmps.csv
```

## Expected output

The highest Ω decile should have a substantially higher future event rate than lower Ω deciles.

The reference reproduction reports approximately:

```text
Top Omega decile:   0.0114
Lower Omega deciles: 0.0010
Ratio: ~11.24×
```

Exact numerical equality is not required. The target is regime-like separation.

## Repository structure

```text
omega_core/     reusable functions
examples/       executable reproduction scripts
tests/          minimal tests
paper/          JOSS paper draft
data/           local data directory
```

## Reproducibility

The full data/code/procedure package is archived separately on Zenodo.

## License

MIT
