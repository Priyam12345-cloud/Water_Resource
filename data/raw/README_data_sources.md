# Data You Need to Download

## 1) Rainfall Data (mandatory)
- Preferred source: IMD station data for Mumbai (hourly if possible).
- Backup source: vetted open dataset from Kaggle or government open data portals.
- You should create an event-based table with columns matching `rainfall_events.csv`.

## 2) Catchment Area and Land Use (mandatory)
- Source used in this repo: GHSL Urban Centre Database (UCDB) R2024A.
- Downloaded regional file (Central and Southern Asia):
	- https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_UCDB_GLOBE_R2024A/GHS_UCDB_REGION_GLOBE_R2024A/GHS_UCDB_REGION_CENTRAL_AND_SOUTHERN_ASIA_R2024A/V1-1/GHS_UCDB_REGION_CENTRAL_AND_SOUTHERN_ASIA_R2024A_V1_1.zip
- Extracted workbook expected at:
	- `data/external/ucdb/temp/GHS_UCDB_REGION_CENTRAL_AND_SOUTHERN_ASIA_R2024A.xlsx`
- Run:
	- `python scripts/prepare_ucdb_landuse.py`
- This extracts Mumbai (`ID_UC_G0 = 7599`) fields from `GHSL` sheet:
	- `GC_UCA_KM2_2025`, `GH_BUS_TOT_2000`, `GH_BUS_TOT_2025`
- Then it creates:
	- `data/raw/ucdb_mumbai_metrics.csv`
	- `data/raw/landuse_scenarios.csv`

## 3) Optional Validation Data
- Flood occurrence dates and high-water marks from reports/news archives.
- Helps in qualitative discussion and conclusion.

## Required file names for this project pipeline
- `data/raw/rainfall_events.csv`
- `data/raw/landuse_scenarios.csv`

## If you are using NASA POWER daily rainfall
- Keep the downloaded NASA file at:
	- `data/POWER_Point_Daily_20000101_20241231_019d08N_072d88E_LST.csv`
- Run:
	- `python scripts/prepare_nasa_events.py`
- This creates `data/raw/rainfall_events.csv` using top monsoon daily rainfall events.
- Assumption used: daily rainfall depth is converted to average 24-hour intensity.

Copy templates and rename:
- `rainfall_events_template.csv` -> `rainfall_events.csv`
- `landuse_scenarios_template.csv` -> `landuse_scenarios.csv`
