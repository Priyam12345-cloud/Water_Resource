# Analysis of Rainfall Variability and Its Impact on Runoff Generation in an Urban Catchment

**Individual Report: Anjali Jangid (23B0625)**  
**Course:** Water Resource Engineering (CE 343)  
**Submitted to:** Riddhi Singh  
**Submission Type:** Team project individual report (member-specific)

---

## Team Information

- Anjali Jangid — 23B0625
- Priyam Raj — 23B0626

---

## 1. Project Overview (Brief)

This project evaluates how rainfall variability and urbanization together affect runoff generation in an urban catchment, using Mumbai as the case study. The team used open-source rainfall and urban land-use datasets, applied the Rational Method, and compared pre-urban and post-urban scenarios.

---

## 2. My Individual Contributions (Anjali)

As per team allocation and execution, my major contributions were:

1. Collection and preprocessing of rainfall and land-use inputs for the selected study area.
2. Verification and quality checks of key input files and generated tables.
3. Computation review and validation of peak discharge outputs for pre-urban and post-urban scenarios.
4. Graphical analysis and interpretation support for runoff comparison and trend behavior.
5. Co-authoring interpretation and conclusion sections with focus on flood-risk implications.

---

## 3. Data Work Done by Me

### 3.1 Rainfall and event dataset checks

I verified the event dataset generated from NASA POWER rainfall data and checked that event fields are consistent (`event_id`, date, duration, rainfall depth, and intensity). I reviewed resulting event entries used in runoff estimation.

- Input rainfall file: `data/POWER_Point_Daily_20000101_20241231_019d08N_072d88E_LST.csv`
- Event file used in analysis: `data/raw/rainfall_events.csv`

### 3.2 Land-use and urbanization input checks

I reviewed the urban land-use inputs derived from JRC GHS-UCDB and confirmed Mumbai scenario values were correctly carried into model input files used for pre/post comparison.

- UCDB source workbook used in workflow: `data/external/ucdb/temp/GHS_UCDB_REGION_CENTRAL_AND_SOUTHERN_ASIA_R2024A.xlsx`
- Scenario input used in model: `data/raw/landuse_scenarios.csv`

---

## 4. Methods Focus (My Role)

Although model implementation was led by Priyam, I focused on method-side data reliability and output consistency checks before and after runs.

### 4.1 Rational Method context

The team used:

\[
Q_p = 0.278 \cdot C \cdot I \cdot A
\]

Where:
- \(Q_p\): peak discharge (m3/s)
- \(C\): weighted runoff coefficient
- \(I\): rainfall intensity (mm/hr)
- \(A\): catchment area (km2)

My method-level contribution was validating that the required inputs for \(C\), \(I\), and \(A\) are coherent and correctly propagated into final result tables.

### 4.2 Scenario comparison checks

I specifically checked output consistency for:
- pre-urban vs post-urban peak discharge values,
- delta runoff values, and
- percent increase trends across all events.

Primary file reviewed:
- `outputs/tables/pre_post_comparison.csv`

---

## 5. Results (From My Analysis View)

### 5.1 Core summary (reviewed and interpreted)

From generated outputs:
- Number of analyzed events: 12
- Mean pre-urban discharge: ~635.54 m3/s
- Mean post-urban discharge: ~657.51 m3/s
- Mean increase: ~21.97 m3/s
- Mean percent increase: ~3.46%

(Reference file: `outputs/tables/extended_summary.csv`)

### 5.2 Graphical analysis completed/reviewed by me

I worked on figure-level interpretation and trend communication for submission, including:
- pre vs post distribution comparison,
- percent increase spread,
- intensity vs runoff-change relation,
- ranking of high-impact events.

Key figures:
- `outputs/figures/extended_box_pre_post.png`
- `outputs/figures/extended_hist_percent_increase.png`
- `outputs/figures/extended_scatter_intensity_delta.png`
- `outputs/figures/extended_top10_percent_increase.png`
- `outputs/figures/event_peak_discharge_comparison.png`

### 5.3 Interpretation by me

My interpretation is that urbanization in the selected Mumbai urban center increases runoff response consistently across events. Even where percentage increases are moderate, the absolute increase in peak discharge is important for drainage and flood-risk planning, especially during intense events.

---

## 6. Brief Team Synthesis

As a team, we established a reproducible pipeline from real open data to event runoff comparison and sensitivity analysis. Priyam led model/sensitivity implementation, and I led data handling checks, peak-output validation, graph-based analysis, and interpretation framing. Together, we conclude that urbanization has a measurable adverse effect on peak runoff in the study case.

---

## 7. Limitations and Recommendations

### Limitations
- Point-based rainfall source may not represent full spatial variability over the urban catchment.
- Rational Method provides a practical comparative framework but is simplified.
- Local calibration with observed flow data is not included.

### Recommendations
- Add gauge-based spatial rainfall where available.
- Use calibrated/event-based hydrologic model for design-level applications.
- Extend analysis with return-period linked storm characterization.

---

## 8. Reproducibility References (Project Files)

- Main model: `scripts/runoff_analysis.py`
- Event preparation: `scripts/prepare_nasa_events.py`
- Urban scenario preparation: `scripts/ucdb_to_landuse.py`
- Extended plots: `scripts/extended_analysis.py`
- Sensitivity/uncertainty: `scripts/sensitivity_uncertainty.py`

---

## 9. Declaration

This report is my individual team-member submission highlighting my own methods/results contributions, while briefly synthesizing overall team outcomes, as instructed for CE343 team projects.
