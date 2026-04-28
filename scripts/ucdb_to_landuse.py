#!/usr/bin/env python3
"""
Extract Mumbai (ID 7599) from the UCDB workbook and compute
impervious fractions and weighted runoff coefficients.

Writes `data/raw/landuse_scenarios.csv` with two scenarios: pre_urban and post_urban.

Assumptions:
- Built-up surface from GHSL (m2) divided by UC area (km2 -> m2) => impervious fraction
- Runoff mapping: impervious C = 0.95, pervious C = 0.30 (literature-based defaults)

Run as: python scripts/ucdb_to_landuse.py
"""
import os
import sys
import pandas as pd


def find_col(cols, candidates):
    for c in candidates:
        if c in cols:
            return c
    return None


def main(xlsx_path='data/external/ucdb/temp/GHS_UCDB_REGION_CENTRAL_AND_SOUTHERN_ASIA_R2024A.xlsx', mumbai_id=7599):
    if not os.path.exists(xlsx_path):
        print('UCDB workbook not found:', xlsx_path)
        sys.exit(2)

    # Read headers to safely discover column names
    gc_cols = pd.read_excel(xlsx_path, sheet_name='GENERAL_CHARACTERISTICS', nrows=0).columns.tolist()
    ghsl_cols = pd.read_excel(xlsx_path, sheet_name='GHSL', nrows=0).columns.tolist()

    id_col_gc = find_col(gc_cols, ['ID_UC_G0', 'ID_UC_G1', 'ID_UC'])
    area_col = find_col(gc_cols, ['GC_UCA_KM2_2025', 'GC_UCA_KM2', 'GC_UCA_KM2_2015', 'GC_UCA_KM2_2020'])

    id_col_ghsl = find_col(ghsl_cols, ['ID_UC_G0', 'ID_UC_G1', 'ID_UC'])
    gh_bus_2000 = find_col(ghsl_cols, ['GH_BUS_TOT_2000', 'GH_BUS_TOT_2000_M2', 'GH_BU_TOT_2000'])
    gh_bus_2020 = find_col(ghsl_cols, ['GH_BUS_TOT_2020', 'GH_BUS_TOT_2020_M2', 'GH_BU_TOT_2020'])
    gh_bus_2025 = find_col(ghsl_cols, ['GH_BUS_TOT_2025', 'GH_BUS_TOT_2025_M2', 'GH_BU_TOT_2025'])

    if id_col_gc is None:
        print('Could not find ID column in GENERAL_CHARACTERISTICS sheet')
        sys.exit(3)

    gc_usecols = [c for c in [id_col_gc, area_col] if c]
    ghsl_usecols = [c for c in [id_col_ghsl, gh_bus_2000, gh_bus_2020, gh_bus_2025] if c]

    df_gc = pd.read_excel(xlsx_path, sheet_name='GENERAL_CHARACTERISTICS', usecols=gc_usecols)
    df_ghsl = pd.read_excel(xlsx_path, sheet_name='GHSL', usecols=ghsl_usecols)

    # merge on ID
    left = id_col_gc
    right = id_col_ghsl if id_col_ghsl in df_ghsl.columns else id_col_gc
    df = pd.merge(df_gc, df_ghsl, left_on=left, right_on=right, how='inner')

    # find Mumbai row
    row = df[df[left] == mumbai_id]
    if row.empty:
        row = df[df[left].astype(str) == str(mumbai_id)]
    if row.empty:
        print('Mumbai with id', mumbai_id, 'not found in UCDB sheets')
        sys.exit(4)

    area_km2 = float(row[area_col].iloc[0]) if area_col in row.columns else None

    def val(col):
        if col and col in row.columns and pd.notna(row[col].iloc[0]):
            return float(row[col].iloc[0])
        return None

    built2000 = val(gh_bus_2000)
    built2020 = val(gh_bus_2020)
    built2025 = val(gh_bus_2025) or built2020

    if area_km2 is None:
        print('Area column not found or empty')
        sys.exit(5)

    area_m2 = area_km2 * 1e6
    if built2000 is None or built2025 is None:
        print('Built-up values for 2000 or 2025 missing; available columns:', ghsl_usecols)

    imp_pre = (built2000 / area_m2) if built2000 is not None else 0.0
    imp_post = (built2025 / area_m2) if built2025 is not None else imp_pre

    # Mapping assumptions (documented): impervious surfaces ~0.95, pervious ~0.30
    C_imp = 0.95
    C_perv = 0.30
    C_pre = C_imp * imp_pre + C_perv * (1 - imp_pre)
    C_post = C_imp * imp_post + C_perv * (1 - imp_post)

    out_csv = 'data/raw/landuse_scenarios.csv'
    df_out = pd.DataFrame([
        {
            'scenario': 'pre_urban',
            'area_km2': area_km2,
            'impervious_fraction': round(imp_pre, 4),
            'pervious_fraction': round(1 - imp_pre, 4),
            'runoff_coefficient_weighted': round(C_pre, 3),
        },
        {
            'scenario': 'post_urban',
            'area_km2': area_km2,
            'impervious_fraction': round(imp_post, 4),
            'pervious_fraction': round(1 - imp_post, 4),
            'runoff_coefficient_weighted': round(C_post, 3),
        },
    ])

    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    df_out.to_csv(out_csv, index=False)

    print('Wrote', out_csv)
    print(df_out.to_string(index=False))


if __name__ == '__main__':
    main()
