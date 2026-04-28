# CE343: Rainfall Variability and Urban Runoff (Mumbai Case Study)

## What is prepared
- Input templates for rainfall events and land-use scenarios.
- A Python script that computes peak discharge for pre-urban and post-urban conditions.
- Sensitivity analysis for rainfall intensity and runoff coefficient.
- Auto-generated output tables and figures.
- Technical paper outline.

![Figure 3. Monte Carlo distribution of the mean percent increase in peak discharge due to urbanization.](outputs/figures/sensitivity_hist_mean_percent_increase.png)

![Figure 1. Peak discharge comparison for pre-urban and post-urban scenarios across the selected storm events in Mumbai.](outputs/figures/extended_box_pre_post.png)
## Folder structure
- `data/raw/`: input CSV files
- `data/processed/`: optional cleaned data
- `scripts/`: analysis scripts
- `outputs/tables/`: result tables
- `outputs/figures/`: result plots
- `report/`: paper drafting materials

## Data files required
Create these files in `data/raw/`:
1. `rainfall_events.csv`
2. `landuse_scenarios.csv`

Note: template files were removed from the repository and replaced by UCDB-derived land-use processing. Used the provided scripts to generate files from source data (NASA POWER and JRC GHS-UCDB).

## Recommended data source list
See: `data/raw/README_data_sources.md`

## Run steps
1. Install Python packages:
   - `pip install -r requirements.txt`
2. If using NASA POWER daily rainfall file already placed in `data/`:
   - `python scripts/prepare_nasa_events.py`
3. If using downloaded UCDB workbook for Mumbai land-use:
   - `python scripts/ucdb_to_landuse.py`
4. Run:
   - `python scripts/runoff_analysis.py`

## Rational Method used
Qp = 0.278 * C * I * A
- Qp in m3/s
- C: weighted runoff coefficient
- I: rainfall intensity (mm/hr)
- A: catchment area (km2)

## Outputs generated
- `outputs/tables/all_event_scenario_discharge.csv`
- `outputs/tables/pre_post_comparison.csv`
- `outputs/tables/sensitivity_intensity.csv`
- `outputs/tables/sensitivity_coefficient.csv`
- `outputs/tables/summary_stats.csv`
- `outputs/figures/event_peak_discharge_comparison.png`
- `outputs/figures/sensitivity_intensity.png`
- `outputs/figures/sensitivity_coefficient.png`

## Team mapping (from your proposal)
- Anjali: data collection, discharge computation table, graphing, interpretation
- Priyam: intensity estimation, model setup, sensitivity analysis
- Both: final technical paper

