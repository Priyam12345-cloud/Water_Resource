# Analysis of Rainfall Variability and Its Impact on Runoff Generation in an Urban Catchment

**Course:** Water Resource Engineering (CE 343)

**Submitted to:** Riddhi Singh

**Team:**
- Anjali Jangid — 23B0625
- Priyam Raj — 23B0626

---

## Abstract

This report (Priyam Raj contribution) documents the data processing, modelling, and sensitivity analysis performed to evaluate how urbanization affects rainfall–runoff response in Mumbai. Using NASA POWER rainfall and JRC GHS‑UCDB built‑up data, we computed event intensities, derived impervious fractions, and applied the Rational Method to estimate peak discharges for pre‑ and post‑urban scenarios. A Monte Carlo sensitivity analysis quantifies uncertainty from runoff coefficients and rainfall intensity variability.

## Data Sources

- Rainfall: NASA POWER daily point product (local file: data/POWER_Point_Daily_20000101_20241231_019d08N_072d88E_LST.csv). Processed events: [data/raw/rainfall_events.csv](data/raw/rainfall_events.csv).
- Land use / built‑up: JRC GHS‑UCDB R2024A (regional workbook used: data/external/ucdb/temp/GHS_UCDB_REGION_CENTRAL_AND_SOUTHERN_ASIA_R2024A.xlsx). The UCDB record for Mumbai (ID 7599) was used to compute impervious fractions.

## Methods (Priyam)

1. Event extraction: daily precipitation was converted to discrete storm events with durations and intensities (`scripts/prepare_nasa_events.py`).
2. Land‑use conversion: `scripts/ucdb_to_landuse.py` extracts built‑up area and urban area from UCDB and computes impervious_fraction = built_up_m2 / (area_km2 * 1e6). Weighted runoff coefficients are computed with C_imp = 0.95 and C_perv = 0.30 as documented in the script. Output: [data/raw/landuse_scenarios.csv](data/raw/landuse_scenarios.csv#L1-L3).
3. Peak discharge: Rational Method (SI) with Qp = 0.278 * C * I * A (scripts/runoff_analysis.py). Area `A` in km², intensity `I` in mm/hr, produces Qp in m³/s.
4. Sensitivity/uncertainty: Monte Carlo sampling of C_imp ~ N(0.95,0.03) truncated, C_perv ~ N(0.30,0.05) truncated, and intensity multiplier ~ N(1,0.1) applied event-wise. The analysis (scripts/sensitivity_uncertainty.py) produced distributions of mean percent increase (post vs pre) and saved results in `outputs/tables/sensitivity_summary.csv`.

## Results

- UCDB‑derived land‑use scenarios: [data/raw/landuse_scenarios.csv](data/raw/landuse_scenarios.csv#L1-L3)
  - `pre_urban`: impervious_fraction ≈ 0.162, C ≈ 0.405
  - `post_urban`: impervious_fraction ≈ 0.1828, C ≈ 0.419

- Event summary (12 events): [outputs/tables/pre_post_comparison.csv](outputs/tables/pre_post_comparison.csv#L1-L12)

- Aggregate statistics: [outputs/tables/extended_summary.csv](outputs/tables/extended_summary.csv#L1-L2)
  - n_events = 12
  - mean_pre = 635.54 m3/s
  - mean_post = 657.51 m3/s
  - mean_delta ≈ 21.97 m3/s
  - mean percent increase ≈ 3.46%

- Sensitivity Monte Carlo (2000 samples): [outputs/tables/sensitivity_summary.csv](outputs/tables/sensitivity_summary.csv)
  - Mean of mean percent increase = 3.402% (std = 0.656%)
  - 5th–95th percentile ≈ 2.47% – 4.59%

### Key figures (open these files)
- Boxplot pre vs post: [outputs/figures/extended_box_pre_post.png](outputs/figures/extended_box_pre_post.png)
- Histogram percent increase: [outputs/figures/extended_hist_percent_increase.png](outputs/figures/extended_hist_percent_increase.png)
- Intensity vs ΔQ scatter: [outputs/figures/extended_scatter_intensity_delta.png](outputs/figures/extended_scatter_intensity_delta.png)
- CDF post peaks: [outputs/figures/extended_cdf_post_peak.png](outputs/figures/extended_cdf_post_peak.png)
- Top 10 percent increase: [outputs/figures/extended_top10_percent_increase.png](outputs/figures/extended_top10_percent_increase.png)
- Sensitivity histogram: [outputs/figures/sensitivity_hist_mean_percent_increase.png](outputs/figures/sensitivity_hist_mean_percent_increase.png)

## Discussion (Priyam)

The Monte Carlo analysis shows that uncertainties in component runoff coefficients and plausible intensity variability produce modest uncertainty around the mean percent increase; the 90% interval for the mean percent increase is approximately 2.5–4.6%. This reinforces that—given the relatively small change in impervious fraction detected in UCDB—the expected increase in peak discharge is robust but modest.

## Limitations

- Single‑point rainfall (NASA POWER) rather than spatial gauge network.
- Rational Method simplifications; results are scenario‑comparative rather than detailed hydraulic design outputs.
- Component coefficient priors (C_imp, C_perv) are literature defaults; local calibration would reduce uncertainty.

## Conclusions and Recommendations

Urbanization as quantified increases peak discharges consistently across sampled storms; the effect magnitude is moderate for Mumbai given UCDB built‑up changes. For stronger conclusions, use spatial rainfall data, hydrologic models (SCS‑CN or distributed models), and local calibration with observed discharge records.

## Individual contributions

- **Priyam Raj (23B0626)** — event extraction, Rational Method implementation, UCDB→landuse automation, sensitivity/uncertainty analysis, drafting methods and results.
- **Anjali Jangid (23B0625)** — data acquisition and verification, figure preparation, interpretation, and drafting discussion and conclusions.

## How to reproduce

Run these commands in the repo root:

```bash
python scripts/ucdb_to_landuse.py
python scripts/prepare_nasa_events.py
python scripts/runoff_analysis.py
python scripts/extended_analysis.py
python scripts/sensitivity_uncertainty.py
```

## Files to review

- `data/raw/landuse_scenarios.csv` — UCDB-derived C values
- `outputs/tables/pre_post_comparison.csv` — event-level results
- `outputs/tables/extended_summary.csv`, `outputs/tables/sensitivity_summary.csv`
- `outputs/figures/` — generated plots

## References

- NASA POWER dataset (daily point product) — processed locally. 
- JRC GHS‑UCDB R2024A — regional urban centre database.
- Standard Rational Method formula (textbook references; HEC and urban hydrology manuals).

---

*Report generated automatically from repository scripts (Priyam Raj).* 
