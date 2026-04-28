import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
TABLE_DIR = BASE_DIR / "outputs" / "tables"
FIG_DIR = BASE_DIR / "outputs" / "figures"

RAINFALL_FILE = RAW_DIR / "rainfall_events.csv"
LANDUSE_FILE = RAW_DIR / "landuse_scenarios.csv"


def ensure_dirs() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame]:
    if not RAINFALL_FILE.exists() or not LANDUSE_FILE.exists():
        raise FileNotFoundError(
            "Input files not found. Please create:\n"
            "- data/raw/rainfall_events.csv\n"
            "- data/raw/landuse_scenarios.csv\n"
            "You can start from the provided template CSV files."
        )

    rainfall = pd.read_csv(RAINFALL_FILE)
    landuse = pd.read_csv(LANDUSE_FILE)

    required_rain = {
        "event_id",
        "event_date",
        "duration_hr",
        "rainfall_mm",
        "intensity_mm_per_hr",
    }
    required_land = {
        "scenario",
        "area_km2",
        "runoff_coefficient_weighted",
    }

    if not required_rain.issubset(rainfall.columns):
        missing = required_rain - set(rainfall.columns)
        raise ValueError(f"Missing columns in rainfall file: {sorted(missing)}")

    if not required_land.issubset(landuse.columns):
        missing = required_land - set(landuse.columns)
        raise ValueError(f"Missing columns in land use file: {sorted(missing)}")

    return rainfall, landuse


def compute_discharge(rainfall: pd.DataFrame, landuse: pd.DataFrame) -> pd.DataFrame:
    scenarios = landuse[["scenario", "area_km2", "runoff_coefficient_weighted"]].copy()
    scenarios = scenarios.rename(columns={"runoff_coefficient_weighted": "C"})

    # Cartesian merge: every event evaluated for every scenario.
    rainfall["key"] = 1
    scenarios["key"] = 1
    merged = rainfall.merge(scenarios, on="key").drop(columns="key")

    # Rational Method (SI): Qp (m3/s) = 0.278 * C * I(mm/hr) * A(km2)
    merged["Q_peak_m3_per_s"] = (
        0.278 * merged["C"] * merged["intensity_mm_per_hr"] * merged["area_km2"]
    )

    return merged


def make_comparison_table(result: pd.DataFrame) -> pd.DataFrame:
    pivot = result.pivot_table(
        index=["event_id", "event_date", "intensity_mm_per_hr"],
        columns="scenario",
        values="Q_peak_m3_per_s",
        aggfunc="first",
    ).reset_index()

    required = {"pre_urban", "post_urban"}
    if required.issubset(set(pivot.columns)):
        pivot["delta_m3_per_s"] = pivot["post_urban"] - pivot["pre_urban"]
        pivot["percent_increase"] = (pivot["delta_m3_per_s"] / pivot["pre_urban"]) * 100

    return pivot


def sensitivity_analysis(landuse: pd.DataFrame, baseline_I: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    records_i = []
    records_c = []

    multipliers = [0.8, 0.9, 1.0, 1.1, 1.2]

    for _, row in landuse.iterrows():
        scenario = row["scenario"]
        area = row["area_km2"]
        c_base = row["runoff_coefficient_weighted"]

        for m in multipliers:
            i_var = baseline_I * m
            q_i = 0.278 * c_base * i_var * area
            records_i.append(
                {
                    "scenario": scenario,
                    "intensity_factor": m,
                    "intensity_mm_per_hr": i_var,
                    "Q_peak_m3_per_s": q_i,
                }
            )

        for m in multipliers:
            c_var = c_base * m
            q_c = 0.278 * c_var * baseline_I * area
            records_c.append(
                {
                    "scenario": scenario,
                    "coefficient_factor": m,
                    "C_value": c_var,
                    "Q_peak_m3_per_s": q_c,
                }
            )

    return pd.DataFrame(records_i), pd.DataFrame(records_c)


def make_plots(comp: pd.DataFrame, sens_i: pd.DataFrame, sens_c: pd.DataFrame) -> None:
    sns.set_theme(style="whitegrid")

    if {"pre_urban", "post_urban"}.issubset(comp.columns):
        plot_df = comp.melt(
            id_vars=["event_id", "event_date"],
            value_vars=["pre_urban", "post_urban"],
            var_name="scenario",
            value_name="Q_peak_m3_per_s",
        )

        plt.figure(figsize=(10, 5))
        sns.barplot(data=plot_df, x="event_id", y="Q_peak_m3_per_s", hue="scenario")
        plt.title("Peak Discharge by Event: Pre-Urban vs Post-Urban")
        plt.xlabel("Storm Event")
        plt.ylabel("Peak Discharge (m3/s)")
        plt.tight_layout()
        plt.savefig(FIG_DIR / "event_peak_discharge_comparison.png", dpi=200)
        plt.close()

    plt.figure(figsize=(8, 5))
    sns.lineplot(
        data=sens_i,
        x="intensity_mm_per_hr",
        y="Q_peak_m3_per_s",
        hue="scenario",
        marker="o",
    )
    plt.title("Sensitivity of Peak Discharge to Rainfall Intensity")
    plt.xlabel("Rainfall Intensity (mm/hr)")
    plt.ylabel("Peak Discharge (m3/s)")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "sensitivity_intensity.png", dpi=200)
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.lineplot(
        data=sens_c,
        x="C_value",
        y="Q_peak_m3_per_s",
        hue="scenario",
        marker="o",
    )
    plt.title("Sensitivity of Peak Discharge to Runoff Coefficient")
    plt.xlabel("Runoff Coefficient (C)")
    plt.ylabel("Peak Discharge (m3/s)")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "sensitivity_coefficient.png", dpi=200)
    plt.close()


def main() -> None:
    ensure_dirs()
    rainfall, landuse = load_inputs()

    result = compute_discharge(rainfall, landuse)
    comparison = make_comparison_table(result)

    baseline_intensity = float(rainfall["intensity_mm_per_hr"].mean())
    sens_i, sens_c = sensitivity_analysis(landuse, baseline_intensity)

    result.to_csv(TABLE_DIR / "all_event_scenario_discharge.csv", index=False)
    comparison.to_csv(TABLE_DIR / "pre_post_comparison.csv", index=False)
    sens_i.to_csv(TABLE_DIR / "sensitivity_intensity.csv", index=False)
    sens_c.to_csv(TABLE_DIR / "sensitivity_coefficient.csv", index=False)

    make_plots(comparison, sens_i, sens_c)

    summary = {
        "n_events": rainfall["event_id"].nunique(),
        "baseline_intensity_mm_per_hr": baseline_intensity,
    }

    pd.DataFrame([summary]).to_csv(TABLE_DIR / "summary_stats.csv", index=False)

    print("Analysis complete.")
    print(f"Tables saved in: {TABLE_DIR}")
    print(f"Figures saved in: {FIG_DIR}")


if __name__ == "__main__":
    main()
