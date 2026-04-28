#!/usr/bin/env python3
"""
Monte Carlo sensitivity and uncertainty analysis for runoff peaks.

Generates distributions of percent increase (post vs pre) by sampling C_imp, C_perv,
and rainfall intensity multiplier. Saves summary CSV and figures to outputs.

Run: python scripts/sensitivity_uncertainty.py
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def run_mc(niter=2000, seed=2026):
    np.random.seed(seed)
    # Read inputs
    events = pd.read_csv('data/raw/rainfall_events.csv')
    lu = pd.read_csv('data/raw/landuse_scenarios.csv')

    # get impervious fractions
    imp_pre = float(lu.loc[lu['scenario']=='pre_urban','impervious_fraction'].iloc[0])
    imp_post = float(lu.loc[lu['scenario']=='post_urban','impervious_fraction'].iloc[0])
    area_km2 = float(lu.loc[lu['scenario']=='pre_urban','area_km2'].iloc[0])

    # baseline intensity per event
    I_base = events['intensity_mm_per_hr'].values

    # storage
    mean_percent_increases = np.zeros(niter)
    median_percent_increases = np.zeros(niter)
    per_event_percentiles = []

    for i in range(niter):
        # sample C_imp ~ Normal(0.95, 0.03) truncated [0.8,1.0]
        C_imp = np.clip(np.random.normal(0.95, 0.03), 0.8, 1.0)
        # sample C_perv ~ Normal(0.30, 0.05) truncated [0.0,0.6]
        C_perv = np.clip(np.random.normal(0.30, 0.05), 0.0, 0.6)
        # sample intensity multiplier ~ Lognormal-like via normal around 1 with sd 0.1
        I_mult = np.random.normal(1.0, 0.1, size=I_base.shape)
        I_sample = I_base * I_mult

        # compute weighted C
        Cpre = C_imp * imp_pre + C_perv * (1 - imp_pre)
        Cpost = C_imp * imp_post + C_perv * (1 - imp_post)

        # rational method Qp = 0.278 * C * I * A
        Qpre = 0.278 * Cpre * I_sample * area_km2
        Qpost = 0.278 * Cpost * I_sample * area_km2

        percent_increase = ((Qpost - Qpre) / Qpre) * 100.0
        mean_percent_increases[i] = np.nanmean(percent_increase)
        median_percent_increases[i] = np.nanmedian(percent_increase)
        per_event_percentiles.append(np.nanpercentile(percent_increase, [5,50,95], axis=None))

    per_event_percentiles = np.array(per_event_percentiles)  # niter x 3

    # summary
    summary = {
        'mean_percent_increase_mean': float(np.mean(mean_percent_increases)),
        'mean_percent_increase_std': float(np.std(mean_percent_increases)),
        'mean_percent_increase_p5': float(np.percentile(mean_percent_increases,5)),
        'mean_percent_increase_p50': float(np.percentile(mean_percent_increases,50)),
        'mean_percent_increase_p95': float(np.percentile(mean_percent_increases,95)),
        'median_percent_increase_mean': float(np.mean(median_percent_increases)),
    }

    os.makedirs('outputs/tables', exist_ok=True)
    pd.DataFrame([summary]).to_csv('outputs/tables/sensitivity_summary.csv', index=False)

    # plot histogram of mean percent increases
    os.makedirs('outputs/figures', exist_ok=True)
    fig, ax = plt.subplots(figsize=(6,4))
    sns.histplot(mean_percent_increases, bins=40, kde=True, ax=ax)
    ax.set_xlabel('Mean percent increase (%)')
    ax.set_title('MC Distribution of Mean Percent Increase (Post vs Pre)')
    fig.savefig('outputs/figures/sensitivity_hist_mean_percent_increase.png', bbox_inches='tight', dpi=150)
    plt.close(fig)

    # plot CI band for per-event percentiles (5-95)
    p5 = np.percentile(per_event_percentiles[:,0], [5,50,95])
    p50 = np.percentile(per_event_percentiles[:,1], [5,50,95])
    p95 = np.percentile(per_event_percentiles[:,2], [5,50,95])

    ci_df = pd.DataFrame({
        'stat': ['p5','p50','p95'],
        'value5': [p5[0], p50[0], p95[0]],
        'value50': [p5[1], p50[1], p95[1]],
        'value95': [p5[2], p50[2], p95[2]],
    })
    ci_df.to_csv('outputs/tables/sensitivity_per_event_percentiles_summary.csv', index=False)

    # save samples summary (small sample: 2000 rows)
    samples_df = pd.DataFrame({
        'mean_percent_increase': mean_percent_increases,
        'median_percent_increase': median_percent_increases,
    })
    samples_df.to_csv('outputs/tables/sensitivity_samples.csv', index=False)

    print('Sensitivity MC complete. Summary saved to outputs/tables/sensitivity_summary.csv')


if __name__ == '__main__':
    run_mc()
