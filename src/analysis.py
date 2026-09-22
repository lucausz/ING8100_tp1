import pandas as pd
import matplotlib.pyplot as plt
import os


# Adjustable parameters (replicability)
# TODO: Change START_YEAR and END_YEAR for the replicability part of the assignment
START_YEAR = 1959
END_YEAR = 2026
DATA_FILE = "data/owid-co2-data.csv"
OUTPUT_FILE = f"results/co2_temperature_{START_YEAR}_{END_YEAR}.png"


def load_data():
    try:
        df = pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        print("Dataset not found. Check the data/ folder.")
        exit(1)

    return df


def prepare_data(df):

    # Required columns
    columns_needed = ["year", "co2", "temperature_change_from_ghg"]
    df = df[columns_needed]

    # Rename columns
    df = df.rename(columns={
        "year": "Year",
        "co2": "CO2",
        "temperature_change_from_ghg": "Temperature"
    })

    # Cleaning
    df = df.dropna()

    # Time filtering
    df = df[(df["Year"] >= START_YEAR) & (df["Year"] <= END_YEAR)]

    return df


def compute_correlation(data):
    corr = data["CO2"].corr(data["Temperature"])
    print(f"CO2 / Temperature correlation (Canada): {corr:.3f}")
    return corr


def plot_data(data):
    os.makedirs("results", exist_ok=True)

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # CO2
    ax1.plot(data["Year"], data["CO2"], label="CO2 (Mt)")
    ax1.set_xlabel(f"Year ({START_YEAR} - {END_YEAR})")
    ax1.set_ylabel("CO2 (Mt)")

    # Temperature
    ax2 = ax1.twinx()
    ax2.plot(
        data["Year"],
        data["Temperature"],
        linestyle="--",
        label="Temperature (°C)"
    )
    ax2.set_ylabel("Temperature (°C)")

    # Combined legend
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2)

    plt.title(f"CO2 vs Temperature — Canada ({START_YEAR} - {END_YEAR})")
    plt.tight_layout()

    plt.savefig(OUTPUT_FILE)
    print(f"Graph saved: {OUTPUT_FILE}")

    plt.show()


def main():
    print("Analysis for Canada in progress...")

    df = load_data()
    data = prepare_data(df)

    if data.empty:
        print("No data after filtering")
        return

    compute_correlation(data)
    plot_data(data)


if __name__ == "__main__":
    main()