"""
Exploratory Data Analysis (EDA) for Indian House Price Prediction.

This module generates comprehensive visualizations of the house price dataset,
saving all charts to the outputs/charts/ directory. Designed to run with the
Agg backend for non-interactive (server/script) use.

Author: ML Project Team
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving charts

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
import numpy as np
import os
import sys


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

def _get_project_root() -> str:
    """Return the absolute path to the project root directory.

    Works whether the script is executed from the project root or from src/.
    """
    src_dir = os.path.dirname(os.path.abspath(__file__))
    # If we are inside src/, go one level up
    if os.path.basename(src_dir).lower() == "src":
        return os.path.dirname(src_dir)
    return src_dir


PROJECT_ROOT = _get_project_root()
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "house_prices.csv")
CHARTS_DIR = os.path.join(PROJECT_ROOT, "outputs", "charts")

# ---------------------------------------------------------------------------
# Style configuration
# ---------------------------------------------------------------------------

# Professional color palette
PALETTE = sns.color_palette("Set2")
SINGLE_COLOR = "#4C72B0"
CMAP = "coolwarm"

sns.set_theme(
    style="whitegrid",
    palette=PALETTE,
    font_scale=1.1,
    rc={
        "axes.titleweight": "bold",
        "axes.labelweight": "bold",
        "figure.facecolor": "white",
    },
)


# ---------------------------------------------------------------------------
# Utility: price formatter in Lakhs
# ---------------------------------------------------------------------------

def _lakhs_formatter(x: float, _pos: int = 0) -> str:
    """Format a price value into Lakhs (1 Lakh = 1,00,000)."""
    return f"{x / 1e5:.1f}L"


def _apply_lakhs_yaxis(ax: plt.Axes) -> None:
    """Apply the Lakhs formatter to the y-axis of *ax*."""
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(_lakhs_formatter))
    ax.set_ylabel("Price (₹ Lakhs)")


# ---------------------------------------------------------------------------
# Chart generators
# ---------------------------------------------------------------------------

def plot_price_distribution(df: pd.DataFrame, save_path: str) -> None:
    """1. Histogram of house prices with KDE curve."""
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.histplot(
        df["Price"],
        bins=50,
        kde=True,
        color=SINGLE_COLOR,
        edgecolor="white",
        linewidth=0.5,
        ax=ax,
    )
    ax.set_title("Distribution of House Prices")
    ax.set_xlabel("Price (₹)")
    ax.set_ylabel("Frequency")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(_lakhs_formatter))
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
    print(f"  ✓ Saved: {os.path.basename(save_path)}")


def plot_avg_price_by_city(df: pd.DataFrame, save_path: str) -> None:
    """2. Bar chart of average house price by city, sorted descending."""
    city_avg = (
        df.groupby("City")["Price"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(14, 7))
    sns.barplot(
        data=city_avg,
        x="City",
        y="Price",
        palette="viridis",
        edgecolor="black",
        linewidth=0.5,
        ax=ax,
    )
    ax.set_title("Average House Price by City")
    ax.set_xlabel("City")
    _apply_lakhs_yaxis(ax)
    ax.tick_params(axis="x", rotation=45)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
    print(f"  ✓ Saved: {os.path.basename(save_path)}")


def plot_price_vs_area(df: pd.DataFrame, save_path: str) -> None:
    """3. Scatter plot of Super_Built_Up_Area_sqft vs Price, colored by Property_Type."""
    fig, ax = plt.subplots(figsize=(12, 7))
    property_types = df["Property_Type"].unique()
    colors = sns.color_palette("Set2", n_colors=len(property_types))

    for ptype, color in zip(property_types, colors):
        subset = df[df["Property_Type"] == ptype]
        ax.scatter(
            subset["Super_Built_Up_Area_sqft"],
            subset["Price"],
            label=ptype,
            alpha=0.5,
            s=20,
            color=color,
            edgecolors="none",
        )

    ax.set_title("House Price vs Property Area")
    ax.set_xlabel("Super Built-Up Area (sq ft)")
    _apply_lakhs_yaxis(ax)
    ax.legend(title="Property Type", loc="upper left", framealpha=0.9)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
    print(f"  ✓ Saved: {os.path.basename(save_path)}")


def plot_bhk_vs_price(df: pd.DataFrame, save_path: str) -> None:
    """4. Box plot showing price distribution for each BHK category."""
    fig, ax = plt.subplots(figsize=(12, 7))
    order = sorted(df["BHK"].unique())
    sns.boxplot(
        data=df,
        x="BHK",
        y="Price",
        order=order,
        palette="Set2",
        fliersize=2,
        linewidth=0.8,
        ax=ax,
    )
    ax.set_title("BHK vs House Price")
    ax.set_xlabel("BHK")
    _apply_lakhs_yaxis(ax)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
    print(f"  ✓ Saved: {os.path.basename(save_path)}")


def plot_property_type_comparison(df: pd.DataFrame, save_path: str) -> None:
    """5. Bar chart of average price by property type."""
    ptype_avg = (
        df.groupby("Property_Type")["Price"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=ptype_avg,
        x="Property_Type",
        y="Price",
        palette="Set2",
        edgecolor="black",
        linewidth=0.5,
        ax=ax,
    )
    ax.set_title("Average Price by Property Type")
    ax.set_xlabel("Property Type")
    _apply_lakhs_yaxis(ax)
    ax.tick_params(axis="x", rotation=30)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
    print(f"  ✓ Saved: {os.path.basename(save_path)}")


def plot_correlation_heatmap(df: pd.DataFrame, save_path: str) -> None:
    """6. Heatmap of correlations between numerical features including Price."""
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    corr_matrix = df[numerical_cols].corr()

    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap=CMAP,
        center=0,
        square=True,
        linewidths=0.5,
        linecolor="white",
        cbar_kws={"shrink": 0.8},
        ax=ax,
    )
    ax.set_title("Feature Correlation Heatmap")
    plt.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
    print(f"  ✓ Saved: {os.path.basename(save_path)}")


def plot_numerical_distributions(df: pd.DataFrame, save_path: str) -> None:
    """7. Subplots grid showing histograms of all numerical features."""
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    n = len(numerical_cols)
    ncols = 3
    nrows = int(np.ceil(n / ncols))

    fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 4 * nrows))
    axes = axes.flatten()

    for i, col in enumerate(numerical_cols):
        sns.histplot(
            df[col],
            bins=30,
            kde=True,
            color=PALETTE[i % len(PALETTE)],
            edgecolor="white",
            linewidth=0.5,
            ax=axes[i],
        )
        axes[i].set_title(col, fontsize=11, fontweight="bold")
        axes[i].set_xlabel("")
        axes[i].grid(axis="y", alpha=0.3)

    # Hide any unused subplots
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    fig.suptitle("Distribution of Numerical Features", fontsize=15, fontweight="bold", y=1.01)
    plt.tight_layout()
    fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ Saved: {os.path.basename(save_path)}")


def plot_furnishing_vs_price(df: pd.DataFrame, save_path: str) -> None:
    """8. Bar chart of average price by furnishing status."""
    furn_avg = (
        df.groupby("Furnishing_Status")["Price"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=furn_avg,
        x="Furnishing_Status",
        y="Price",
        palette="Set2",
        edgecolor="black",
        linewidth=0.5,
        ax=ax,
    )
    ax.set_title("Average Price by Furnishing Status")
    ax.set_xlabel("Furnishing Status")
    _apply_lakhs_yaxis(ax)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
    print(f"  ✓ Saved: {os.path.basename(save_path)}")


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Load data, create output directory, generate all EDA charts."""
    print("=" * 60)
    print("  Indian House Price Prediction – Exploratory Data Analysis")
    print("=" * 60)

    # ------------------------------------------------------------------
    # 1. Load dataset
    # ------------------------------------------------------------------
    print(f"\n📂 Loading dataset from: {DATA_PATH}")
    if not os.path.isfile(DATA_PATH):
        print(f"❌ ERROR: Dataset not found at {DATA_PATH}")
        sys.exit(1)

    df = pd.read_csv(DATA_PATH)
    print(f"   Loaded {df.shape[0]:,} rows × {df.shape[1]} columns")

    # Quick data summary
    print(f"\n📊 Dataset Overview:")
    print(f"   Numerical columns : {df.select_dtypes(include=[np.number]).columns.tolist()}")
    print(f"   Categorical columns: {df.select_dtypes(exclude=[np.number]).columns.tolist()}")
    print(f"   Missing values     : {df.isnull().sum().sum()}")
    print(f"   Price range        : ₹{df['Price'].min():,.0f} – ₹{df['Price'].max():,.0f}")
    print(f"   Mean price         : ₹{df['Price'].mean():,.0f}")

    # ------------------------------------------------------------------
    # 2. Create output directory
    # ------------------------------------------------------------------
    os.makedirs(CHARTS_DIR, exist_ok=True)
    print(f"\n📁 Charts directory: {CHARTS_DIR}")

    # ------------------------------------------------------------------
    # 3. Generate all charts
    # ------------------------------------------------------------------
    print("\n🎨 Generating charts ...\n")

    plot_price_distribution(
        df, os.path.join(CHARTS_DIR, "price_distribution.png")
    )
    plot_avg_price_by_city(
        df, os.path.join(CHARTS_DIR, "avg_price_by_city.png")
    )
    plot_price_vs_area(
        df, os.path.join(CHARTS_DIR, "price_vs_area.png")
    )
    plot_bhk_vs_price(
        df, os.path.join(CHARTS_DIR, "bhk_vs_price.png")
    )
    plot_property_type_comparison(
        df, os.path.join(CHARTS_DIR, "property_type_comparison.png")
    )
    plot_correlation_heatmap(
        df, os.path.join(CHARTS_DIR, "correlation_heatmap.png")
    )
    plot_numerical_distributions(
        df, os.path.join(CHARTS_DIR, "numerical_distributions.png")
    )
    plot_furnishing_vs_price(
        df, os.path.join(CHARTS_DIR, "furnishing_vs_price.png")
    )

    print(f"\n✅ All 8 charts saved to: {CHARTS_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
