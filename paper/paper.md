---
title: 'omega-repro: A reproducible pipeline for testing structural concentration in high-Omega regimes'
tags:
  - Python
  - reproducibility
  - time series
  - electricity markets
  - open science
authors:
  - name: Hiroaki Aizawa
    affiliation: 1
affiliations:
  - name: Independent researcher
    index: 1
date: 2026-04-28
bibliography: paper.bib
---

# Summary

`omega-repro` is a minimal Python package for testing whether collapse-related events concentrate in high-Omega regimes. The package provides a reproducible pipeline from public PJM real-time locational marginal price data to a fixed structural concentration test. It is not a prediction model. The objective is to compute a state variable, define events independently of that variable, and compare event frequency in the highest-Omega regime against a baseline.

# Statement of need

Empirical studies of extreme or collapse-like events often suffer from unclear definitions, post-hoc threshold choices, and non-reproducible analysis notebooks. `omega-repro` addresses this by fixing a minimal executable workflow: data preprocessing, structural feature construction, Omega computation, independent event definition, lead alignment, and a single comparison metric.

The reference implementation uses PJM electricity market data because it contains a natural cross-sectional structure. For each timestamp, zonal price dispersion and deviation from the system baseline are used to compute:

```text
Omega = sigma_zone × max(p95 - p_RTO, 0)
```

Events are defined independently as extreme values of `p95 / p_RTO`, then shifted forward by six hours. The main output is the event rate by Omega decile and the comparison between the highest Omega decile and all lower deciles.

# Functionality

The package includes functions to:

- load and normalize PJM RT LMP data,
- compute cross-sectional price statistics,
- compute Omega,
- define independent extreme-ratio events,
- align future events with current Omega,
- compute event rates by Omega decile,
- compare top-Omega and lower-Omega regimes.

# Reproducibility

The package is designed to be run locally or in Google Colab. The reference script is:

```bash
python examples/reproduce_pjm.py data/rt_hrl_lmps.csv
```

The expected qualitative result is regime-like concentration: the highest Omega decile has a substantially higher future event rate than lower Omega deciles. Exact numerical equality is not required because public market data extracts and preprocessing choices can vary slightly.

# Limitations

`omega-repro` does not claim predictive performance or universal validity of the Omega formulation. It provides a fixed software pipeline for testing structural concentration under explicitly stated definitions.
