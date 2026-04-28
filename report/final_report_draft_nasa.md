# Analysis of Rainfall Variability and Its Impact on Runoff Generation in an Urban Catchment

## Course
Water Resource Engineering (CE 343)

## Study Summary
This project quantifies how urbanization changes peak runoff in a Mumbai urban catchment using the Rational Method. Daily NASA POWER rainfall data was converted into event-based rainfall for high monsoon events, and runoff was computed for pre-urban and post-urban land-use scenarios derived from the GHSL Urban Centre Database (UCDB) R2024A.

## Data Used
1. Rainfall source: NASA POWER daily precipitation (`PRECTOTCORR`, mm/day) for point location near Mumbai.
2. Land-use and area source: GHSL UCDB R2024A (Mumbai, `ID_UC_G0 = 7599`).
3. Catchment area from UCDB: 738 km2 (`GC_UCA_KM2_2025`).
4. Built-up surface from UCDB GHSL sheet:
   - Year 2000: 119,583,185 m2 (`GH_BUS_TOT_2000`).
   - Year 2025: 134,907,600 m2 (`GH_BUS_TOT_2025`).
5. Derived land-use scenarios:
   - Pre-urban (2000 built-up share): impervious fraction = 0.1620, weighted runoff coefficient $C = 0.3972$.
   - Post-urban (2025 built-up share): impervious fraction = 0.1828, weighted runoff coefficient $C = 0.4097$.

## Event Preparation from NASA Data
1. Read daily rainfall from 2000-2024.
2. Keep monsoon months (June-September).
3. Select 12 highest daily rainfall events.
4. Convert each daily depth to 24-hour intensity:

$$
I = \frac{P_{day}}{24}
$$

where $I$ is in mm/hr and $P_{day}$ is in mm/day.

## Runoff Model
Rational Method (SI form):

$$
Q_p = 0.278\, C\, I\, A
$$

where:
- $Q_p$ = peak discharge (m3/s)
- $C$ = runoff coefficient
- $I$ = rainfall intensity (mm/hr)
- $A$ = catchment area (km2)

For each event, compute $Q_{pre}$ and $Q_{post}$, then:

$$
\Delta Q = Q_{post} - Q_{pre}
$$

$$
\%\ Increase = \frac{Q_{post} - Q_{pre}}{Q_{pre}} \times 100
$$

## Key Results from Generated Outputs
Using file `outputs/tables/pre_post_comparison.csv`:

1. Number of storm events analysed: 12.
2. Mean pre-urban peak discharge: 623.33 m3/s.
3. Mean post-urban peak discharge: 642.88 m3/s.
4. Mean increase in peak discharge: 19.55 m3/s.
5. Mean percentage increase: 3.14%.
6. Maximum post-urban peak discharge: 803.61 m3/s (event N09, date 2007-06-23).

## How "Impact on Runoff Generation" Is Quantified with This Data
The impact is measured by keeping rainfall and catchment area fixed for each storm event and changing only the runoff coefficient between scenarios.

1. For each event, same $I$ and same $A$ are used in both scenarios.
2. Only $C$ changes from pre-urban (0.3972) to post-urban (0.4097).
3. Therefore, change in $Q_p$ is directly attributed to urbanization effect (higher imperviousness).
4. Event-wise and average increase in discharge gives quantitative impact.

Because the Rational Method is linear in $C$, increasing $C$ from 0.3972 to 0.4097 leads to:

$$
\frac{Q_{post}}{Q_{pre}} = \frac{0.4097}{0.3972} \approx 1.0314
$$

which means approximately 3.14% higher peak runoff under post-urban conditions.

## Engineering Interpretation
1. Urbanization substantially increases peak discharge for intense monsoon events.
2. Higher imperviousness reduces infiltration and shortens runoff response time.
3. Existing drainage systems designed for older land-use conditions may become undersized.
4. Results support stronger urban stormwater management, detention, and drainage upgrades.

## Reproducibility Note
The land-use input file `data/raw/landuse_scenarios.csv` is generated directly from downloaded UCDB data using:

- `python scripts/prepare_ucdb_landuse.py`

The rainfall input file `data/raw/rainfall_events.csv` is generated from downloaded NASA POWER data using:

- `python scripts/prepare_nasa_events.py`

## Limitations
1. Rainfall data used is daily, not hourly; this smooths short-duration peaks.
2. Point rainfall may not represent full catchment spatial variability.
3. Coefficients are scenario-level averages, not parcel-level dynamic values.

## Recommended Improvement
Replace NASA daily with IMD hourly station rainfall for final submission to improve event intensity realism and technical rigor.
