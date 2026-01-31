import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from fuzzywuzzy import fuzz
import argparse

def compare_cell(df):
    """Calculate fuzzy distance between consecutive rows along axis 0."""

    result = pd.DataFrame(index=df.index[:-1], columns=df.columns)

    for col in df.columns:
        for i in range(len(df) - 1):
            result.at[df.index[i], col] = fuzz.ratio(
                str(df[col].iloc[i]),
                str(df[col].iloc[i + 1])
            )

    return result.astype(float)


def plot(df, output=None):
    fuzzy_df = compare_cell(df)

    # Average across dim 1
    mean = fuzzy_df.mean(axis=1)
    std = fuzzy_df.std(axis=1)

    x = range(len(mean))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, mean, color="steelblue", linewidth=2, label="Mean fuzzy ratio")
    ax.fill_between(x, mean - std, mean + std, alpha=0.25, color="steelblue", label="±1 SD")
    ax.fill_between(x, mean - 2*std, mean + 2*std, alpha=0.1, color="steelblue", label="±2 SD")

    ax.set_xlabel("Row pair (N, N+1)")
    ax.set_ylabel("Fuzzy match ratio")
    ax.set_title("Row-wise Average Fuzzy Match with Confidence Band")
    ax.legend()
    ax.set_ylim(0, 100)
    plt.tight_layout()
    plt.savefig(output)
    plt.show()

def main():
    """Fuzzy match analysis for consecutive responses in a CSV file.

    Arguments:
        file              Path to CSV file (rows=fields, columns=responses).
                          The file is transposed so each column becomes a row
                          for pairwise comparison.
        --output, -o      Save plot to file instead of displaying.

    """
    parser = argparse.ArgumentParser(
        description="Fuzzy match analysis between consecutive responses in a CSV.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=main.__doc__
    )
    parser.add_argument("file", help="Path to input CSV file")
    parser.add_argument("-o", "--output", default=None,
                        help="Save plot to file (e.g. plot.png) instead of displaying")

    args = parser.parse_args()

    data = pd.read_csv(args.file)
    data = data.T

    fuzzy_matches = compare_cell(data)
    plot(fuzzy_matches, output=args.output)


if __name__ == "__main__":
    main()

