from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"

NASA_FILE = DATA_DIR / "POWER_Point_Daily_20000101_20241231_019d08N_072d88E_LST.csv"
OUTPUT_FILE = RAW_DIR / "rainfall_events.csv"


def _find_data_start(path: Path) -> int:
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if line.strip() == "-END HEADER-":
                return i + 1
    raise ValueError("Could not find '-END HEADER-' marker in NASA file")


def load_nasa_daily(path: Path) -> pd.DataFrame:
    start_row = _find_data_start(path)
    df = pd.read_csv(path, skiprows=start_row)

    required = {"YEAR", "DOY", "PRECTOTCORR"}
    if not required.issubset(df.columns):
        missing = required - set(df.columns)
        raise ValueError(f"Missing NASA columns: {sorted(missing)}")

    df = df.rename(columns={"PRECTOTCORR": "rainfall_mm"})
    df = df[df["rainfall_mm"] >= 0].copy()

    df["date"] = pd.to_datetime(
        df["YEAR"].astype(int).astype(str) + df["DOY"].astype(int).astype(str).str.zfill(3),
        format="%Y%j",
    )

    return df


def select_events(df: pd.DataFrame, n_events: int = 12) -> pd.DataFrame:
    # Monsoon-focused events for Mumbai.
    monsoon = df[df["date"].dt.month.isin([6, 7, 8, 9])].copy()

    # Sort by highest daily rainfall and keep 1-day separation minimum.
    monsoon = monsoon.sort_values("rainfall_mm", ascending=False).reset_index(drop=True)

    chosen_rows = []
    chosen_dates = []
    for _, row in monsoon.iterrows():
        d = row["date"]
        if all(abs((d - existing).days) >= 1 for existing in chosen_dates):
            chosen_rows.append(row)
            chosen_dates.append(d)
        if len(chosen_rows) >= n_events:
            break

    events = pd.DataFrame(chosen_rows).sort_values("date").reset_index(drop=True)

    events["event_id"] = [f"N{idx + 1:02d}" for idx in range(len(events))]
    events["event_date"] = events["date"].dt.strftime("%Y-%m-%d")
    events["duration_hr"] = 24
    events["intensity_mm_per_hr"] = events["rainfall_mm"] / events["duration_hr"]

    return events[["event_id", "event_date", "duration_hr", "rainfall_mm", "intensity_mm_per_hr"]]


def main() -> None:
    if not NASA_FILE.exists():
        raise FileNotFoundError(f"NASA file not found: {NASA_FILE}")

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    daily = load_nasa_daily(NASA_FILE)
    events = select_events(daily, n_events=12)
    events.to_csv(OUTPUT_FILE, index=False)

    print(f"Prepared {len(events)} events from NASA daily rainfall")
    print(f"Saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
