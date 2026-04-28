#!/usr/bin/env python3
"""Extended analysis and plotting for runoff results.

Produces additional figures in `outputs/figures/` and a summary CSV.
Run: python scripts/extended_analysis.py
"""
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def save_fig(fig, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, bbox_inches='tight', dpi=150)
    plt.close(fig)


def main():
    os.makedirs('outputs/figures', exist_ok=True)
    os.makedirs('outputs/tables', exist_ok=True)

    pre_post_path = 'outputs/tables/pre_post_comparison.csv'
    all_event_path = 'outputs/tables/all_event_scenario_discharge.csv'
    rainfall_events_path = 'data/raw/rainfall_events.csv'

    pre_post = pd.read_csv(pre_post_path)
    all_event = pd.read_csv(all_event_path)
    rainfall = pd.read_csv(rainfall_events_path)

    # Boxplot: pre vs post
    df_long = pre_post.melt(id_vars=['event_id', 'event_date'], value_vars=['pre_urban', 'post_urban'],
                            var_name='scenario', value_name='Q_m3_s')
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(x='scenario', y='Q_m3_s', data=df_long, ax=ax)
    ax.set_title('Peak discharge: Pre vs Post Urban')
    save_fig(fig, 'outputs/figures/extended_box_pre_post.png')

    # Histogram: percent increase
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(pre_post['percent_increase'].dropna(), bins=10, kde=True, ax=ax)
    ax.set_xlabel('Percent increase (%)')
    ax.set_title('Distribution of Percent Increase (Post vs Pre)')
    save_fig(fig, 'outputs/figures/extended_hist_percent_increase.png')

    # Scatter: event intensity vs delta
    if 'event_id' in pre_post.columns and 'intensity_mm_per_hr' in pre_post.columns:
        scatter_df = pre_post[['event_id', 'intensity_mm_per_hr', 'delta_m3_per_s', 'percent_increase']].dropna()
    else:
        # try joining with rainfall events
        if 'event_id' in pre_post.columns and 'event_id' in rainfall.columns:
            scatter_df = pre_post.merge(rainfall[['event_id', 'intensity_mm_per_hr']], on='event_id', how='left')
        else:
            scatter_df = pre_post.copy()

    if 'intensity_mm_per_hr' in scatter_df.columns:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.scatterplot(x='intensity_mm_per_hr', y='delta_m3_per_s', data=scatter_df, ax=ax)
        ax.set_xlabel('Intensity (mm/hr)')
        ax.set_ylabel('Delta Q (m3/s)')
        ax.set_title('Event Intensity vs ΔQ (post - pre)')
        save_fig(fig, 'outputs/figures/extended_scatter_intensity_delta.png')

    # CDF of post_urban peaks
    fig, ax = plt.subplots(figsize=(6, 4))
    data = np.sort(pre_post['post_urban'].dropna())
    y = np.arange(1, len(data)+1) / len(data)
    ax.plot(data, y, marker='o')
    ax.set_xlabel('Peak discharge (m3/s)')
    ax.set_ylabel('Cumulative Probability')
    ax.set_title('CDF of Post-Urban Peak Discharge')
    save_fig(fig, 'outputs/figures/extended_cdf_post_peak.png')

    # Top events by percent increase
    top = pre_post.sort_values('percent_increase', ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x='event_id', y='percent_increase', data=top, ax=ax)
    ax.set_xlabel('Event ID')
    ax.set_ylabel('Percent increase (%)')
    ax.set_title('Top 10 Events by Percent Increase')
    plt.xticks(rotation=45)
    save_fig(fig, 'outputs/figures/extended_top10_percent_increase.png')

    # Extended summary CSV
    summary = {
        'n_events': len(pre_post),
        'mean_pre_m3_s': float(pre_post['pre_urban'].mean()),
        'mean_post_m3_s': float(pre_post['post_urban'].mean()),
        'mean_delta_m3_s': float(pre_post['delta_m3_per_s'].mean()),
        'mean_percent_increase': float(pre_post['percent_increase'].mean()),
    }
    pd.DataFrame([summary]).to_csv('outputs/tables/extended_summary.csv', index=False)

    print('Extended analysis complete. Figures saved to outputs/figures and summary to outputs/tables/extended_summary.csv')


if __name__ == '__main__':
    main()
