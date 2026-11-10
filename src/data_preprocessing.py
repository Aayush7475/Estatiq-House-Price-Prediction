"""
data_preprocessing.py - Complete Data Preprocessing Pipeline
=============================================================
Indian House Price Prediction Project

This module handles all data loading, exploration, cleaning, and preprocessing
steps required before feeding data into a machine learning model.

KEY ML CONCEPTS:
- Preprocessing: Raw data is rarely in a format that ML algorithms can directly
  use. We need to convert categorical text into numbers, scale features to
  similar ranges, and handle missing values.
- Pipeline: A sklearn Pipeline chains preprocessing and modeling steps together,
  ensuring that the same transformations are applied consistently during both
  training and prediction (preventing "data leakage").
- Train/Test Split: We hold out a portion of data (20%) that the model never
  sees during training, so we can honestly evaluate how well it generalizes
  to new, unseen data.

Author: ML Project
"""

import os
import sys
import numpy as np
import pandas as pd

# scikit-learn imports for preprocessing and pipeline construction
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


# ---------------------------------------------------------------------------
# Constants: Define column groups once so every function stays consistent
# ---------------------------------------------------------------------------

# The column we want to predict (also called the "label" or "dependent variable")
TARGET_COLUMN = "Price"

# Numerical (continuous or discrete numeric) feature columns
# These will be scaled so that each feature has mean ≈ 0 and std ≈ 1,
# which helps many ML algorithms converge faster and treat all features fairly.
NUMERICAL_COLUMNS = [
    "BHK",                      # Number of Bedrooms, Hall, Kitchen
    "Bathrooms",                # Number of bathrooms
    "Super_Built_Up_Area_sqft", # Total area including walls, balcony, etc.
    "Carpet_Area_sqft",         # Usable floor area inside the walls
    "Property_Age_years",       # Age of the property in years
    "Floor_No",                 # Floor number the property is on
    "Total_Floors",             # Total floors in the building
    "Parking",                  # Number of parking spots (0-3)
    "Lift",                     # Whether lift is available (0 or 1)
    "Gated_Community",          # Whether in a gated community (0 or 1)
]

# Categorical (text-based) feature columns
# These will be one-hot encoded: each unique category becomes its own binary column.
# Example: Furnishing_Status with values [Furnished, Semi-Furnished, Unfurnished]
#          becomes three columns, each being 0 or 1.
CATEGORICAL_COLUMNS = [
    "City",              # City name (10 possible cities)
    "Locality",          # Specific locality/neighborhood (~80 unique values)
    "Property_Type",     # Apartment, Independent House, Villa, Builder Floor
    "Furnishing_Status", # Furnished, Semi-Furnished, Unfurnished
]


def _resolve_data_path(relative_path="data/house_prices.csv"):
    """
    Resolve the path to the dataset CSV file.

    This helper handles two common scenarios:
    1. Script is run from the project root:  python src/data_preprocessing.py
    2. Script is run from the src/ directory: python data_preprocessing.py

    It looks for the CSV relative to the project root by walking up from the
    script's location if needed.

    Parameters
    ----------
    relative_path : str
        Path to the CSV file relative to the project root directory.

    Returns
    -------
    str
        Absolute path to the dataset CSV file.

    Raises
    ------
    FileNotFoundError
        If the CSV file cannot be found in any expected location.
    """
    # Strategy 1: Try relative to the current working directory
    if os.path.isfile(relative_path):
        return os.path.abspath(relative_path)

    # Strategy 2: Try relative to this script's parent directory (project root)
    # If this script lives in <project_root>/src/, go one level up.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)  # Go up from src/ to project root
    candidate = os.path.join(project_root, relative_path)
    if os.path.isfile(candidate):
        return candidate

    # Strategy 3: Maybe the script IS at the project root level
    candidate = os.path.join(script_dir, relative_path)
    if os.path.isfile(candidate):
        return candidate

    raise FileNotFoundError(
        f"Could not find dataset at '{relative_path}'. "
        f"Searched in:\n"
        f"  1. {os.path.abspath(relative_path)}\n"
        f"  2. {os.path.join(project_root, relative_path)}\n"
        f"  3. {os.path.join(script_dir, relative_path)}\n"
        f"Please ensure the CSV file exists at 'data/house_prices.csv' "
        f"relative to the project root."
    )


# ---------------------------------------------------------------------------
# Core Pipeline Functions
# ---------------------------------------------------------------------------

def load_data(filepath=None):
    """
    Load the house prices dataset from a CSV file into a pandas DataFrame.

    A DataFrame is like a spreadsheet in Python — it has rows (individual houses)
    and columns (features like City, BHK, Price, etc.).

    Parameters
    ----------
    filepath : str, optional
        Absolute or relative path to the CSV file. If None, the default
        path 'data/house_prices.csv' is resolved automatically.

    Returns
    -------
    pd.DataFrame
        The loaded dataset with all columns intact.
    """
    if filepath is None:
        filepath = _resolve_data_path()
    else:
        filepath = os.path.abspath(filepath)

    print("=" * 70)
    print("STEP 1: LOADING DATA")
    print("=" * 70)
    print(f"  Source file : {filepath}")

    df = pd.read_csv(filepath)

    print(f"  Rows loaded : {len(df):,}")
    print(f"  Columns     : {len(df.columns)}")
    print(f"  Column names: {list(df.columns)}")
    print()

    return df


def explore_data(df):
    """
    Perform exploratory data analysis (EDA) and print a comprehensive summary.

    EDA is the first thing a data scientist does after loading data. It helps
    you understand:
    - How big is the dataset?
    - What types of data do we have (numbers vs. text)?
    - Are there missing values that need handling?
    - Are there duplicate rows that might bias the model?
    - What are the basic statistics (min, max, mean) of each feature?

    Parameters
    ----------
    df : pd.DataFrame
        The raw dataset to explore.

    Returns
    -------
    None
        Prints all findings to the console.
    """
    print("=" * 70)
    print("STEP 2: EXPLORATORY DATA ANALYSIS (EDA)")
    print("=" * 70)

    # --- Shape: (rows, columns) ---
    print(f"\n📊 Dataset Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

    # --- Data Types ---
    # Each column has a type: int64 (integer), float64 (decimal), object (text)
    print("\n📋 Column Data Types:")
    print("-" * 45)
    for col in df.columns:
        dtype = df[col].dtype
        n_unique = df[col].nunique()
        print(f"  {col:<30s} {str(dtype):<10s} ({n_unique:,} unique)")

    # --- Missing Values ---
    # ML models cannot handle empty cells. We need to know where gaps are
    # so we can fill them (imputation) or drop those rows.
    missing = df.isnull().sum()
    total_missing = missing.sum()
    print(f"\n❓ Missing Values: {total_missing:,} total")
    if total_missing > 0:
        print("-" * 45)
        for col in df.columns:
            if missing[col] > 0:
                pct = 100.0 * missing[col] / len(df)
                print(f"  {col:<30s} {missing[col]:>6,} ({pct:.1f}%)")
    else:
        print("  ✅ No missing values found — great!")

    # --- Duplicates ---
    # Duplicate rows can artificially inflate the model's confidence in
    # certain patterns. It's good practice to check and remove them.
    n_duplicates = df.duplicated().sum()
    print(f"\n🔄 Duplicate Rows: {n_duplicates:,}")
    if n_duplicates > 0:
        print(f"  ⚠️  Consider removing duplicates to avoid bias.")
    else:
        print("  ✅ No duplicate rows found.")

    # --- Basic Statistics for Numerical Columns ---
    # .describe() gives count, mean, std, min, 25%, 50% (median), 75%, max
    print("\n📈 Numerical Feature Statistics:")
    print("-" * 70)
    numerical_cols_present = [c for c in NUMERICAL_COLUMNS + [TARGET_COLUMN] if c in df.columns]
    if numerical_cols_present:
        stats = df[numerical_cols_present].describe().T
        # Format large numbers with commas for readability
        for stat_col in ["mean", "std", "min", "25%", "50%", "75%", "max"]:
            if stat_col in stats.columns:
                stats[stat_col] = stats[stat_col].apply(lambda x: f"{x:,.1f}")
        stats["count"] = stats["count"].apply(lambda x: f"{float(x):,.0f}")
        print(stats.to_string())
    else:
        print("  No numerical columns found.")

    # --- Categorical Column Value Counts ---
    print("\n📝 Categorical Feature Summary:")
    print("-" * 70)
    categorical_cols_present = [c for c in CATEGORICAL_COLUMNS if c in df.columns]
    for col in categorical_cols_present:
        n_unique = df[col].nunique()
        top_value = df[col].mode().iloc[0] if not df[col].mode().empty else "N/A"
        top_count = (df[col] == top_value).sum()
        print(f"  {col:<25s} {n_unique:>4} unique | Most common: '{top_value}' ({top_count:,} times)")

    # --- Target Variable (Price) Summary ---
    if TARGET_COLUMN in df.columns:
        print(f"\n🎯 Target Variable '{TARGET_COLUMN}' Summary:")
        print("-" * 45)
        price = df[TARGET_COLUMN]
        print(f"  Min    : ₹{price.min():>15,.0f}")
        print(f"  Max    : ₹{price.max():>15,.0f}")
        print(f"  Mean   : ₹{price.mean():>15,.0f}")
        print(f"  Median : ₹{price.median():>15,.0f}")
        print(f"  Std Dev: ₹{price.std():>15,.0f}")

    print()


def preprocess_data(df):
    """
    Build the preprocessing pipeline and separate features from the target.

    This is the heart of data preparation. We create a "preprocessor" that will:

    1. CATEGORICAL FEATURES (City, Locality, Property_Type, Furnishing_Status):
       - Impute missing values with the most frequently occurring category.
       - One-Hot Encode: Convert each category into binary (0/1) columns.
         Example: Property_Type='Villa' → [0, 0, 0, 1] for
         [Apartment, Builder Floor, Independent House, Villa]
       - handle_unknown='ignore': If a new category appears in test data that
         wasn't in training, it simply gets all zeros (safe fallback).
       - sparse_output=False: Return a regular dense array, not a sparse matrix.

    2. NUMERICAL FEATURES (BHK, Bathrooms, areas, etc.):
       - Impute missing values with the median (robust to outliers, unlike mean).
       - StandardScaler: Transform each feature to have mean=0 and std=1.
         Formula: z = (x - mean) / std
         Why? Features like Super_Built_Up_Area (500-5000) would dominate
         features like BHK (1-5) without scaling. Scaling puts them on
         equal footing.

    The ColumnTransformer applies different transformations to different column
    groups simultaneously, then concatenates the results.

    IMPORTANT: The preprocessor is returned UNFITTED. It will be fitted on the
    training data only (inside a Pipeline), preventing data leakage from the
    test set.

    Parameters
    ----------
    df : pd.DataFrame
        The full dataset including the target column 'Price'.

    Returns
    -------
    X : pd.DataFrame
        Feature matrix (all columns except 'Price').
    y : pd.Series
        Target vector (the 'Price' column).
    preprocessor : sklearn.compose.ColumnTransformer
        Unfitted preprocessing transformer ready to be used in a Pipeline.
    """
    print("=" * 70)
    print("STEP 3: BUILDING PREPROCESSING PIPELINE")
    print("=" * 70)

    # --- Separate features (X) from target (y) ---
    # X = the inputs the model uses to make predictions
    # y = the output (price) the model tries to predict
    if TARGET_COLUMN not in df.columns:
        raise ValueError(
            f"Target column '{TARGET_COLUMN}' not found in DataFrame. "
            f"Available columns: {list(df.columns)}"
        )

    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]

    print(f"  Features (X) shape : {X.shape}")
    print(f"  Target   (y) shape : {y.shape}")

    # --- Identify which columns are actually present in the data ---
    # This makes the code robust even if some columns are missing from the CSV.
    numerical_cols = [col for col in NUMERICAL_COLUMNS if col in X.columns]
    categorical_cols = [col for col in CATEGORICAL_COLUMNS if col in X.columns]

    print(f"\n  Numerical columns  ({len(numerical_cols)}): {numerical_cols}")
    print(f"  Categorical columns ({len(categorical_cols)}): {categorical_cols}")

    # Check for any columns in the data that we're not handling
    handled_cols = set(numerical_cols + categorical_cols)
    unhandled_cols = [col for col in X.columns if col not in handled_cols]
    if unhandled_cols:
        print(f"\n  ⚠️  Unhandled columns (will be dropped): {unhandled_cols}")

    # --- Build sub-pipelines for each column type ---

    # Numerical pipeline: impute missing → then scale
    # Why median for imputation? The median is less affected by extreme outliers
    # than the mean. If most houses have 2-3 BHK but one has 10, the median
    # still gives a reasonable fill value.
    numerical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    # Categorical pipeline: impute missing → then one-hot encode
    # Why most_frequent for imputation? For categories, we can't take a median.
    # The most common category is a reasonable default assumption.
    categorical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    # --- Combine into a single ColumnTransformer ---
    # The ColumnTransformer applies the right pipeline to the right columns
    # and concatenates all the outputs into one feature matrix.
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numerical_pipeline, numerical_cols),    # Apply numerical pipeline
            ("cat", categorical_pipeline, categorical_cols), # Apply categorical pipeline
        ],
        remainder="drop",  # Drop any columns not listed above (safety net)
        verbose_feature_names_out=True,  # Prefix output column names with transformer name
    )

    print("\n  ✅ Preprocessing pipeline built successfully!")
    print("     Pipeline structure:")
    print("     ┌─ Numerical ──→ MedianImputer → StandardScaler")
    print("     └─ Categorical → MostFreqImputer → OneHotEncoder")
    print()

    return X, y, preprocessor


def split_data(X, y, test_size=0.2, random_state=42):
    """
    Split the dataset into training and testing subsets.

    WHY SPLIT?
    If we train and evaluate on the same data, the model could just memorize
    the training examples (overfitting) and appear to perform perfectly.
    By holding out 20% of data, we get an honest estimate of how well the
    model will perform on genuinely new, unseen houses.

    WHY random_state=42?
    Setting a random seed ensures reproducibility — every time we run this
    code, we get the exact same split. This makes experiments comparable.
    The number 42 is arbitrary (it's a tradition in data science, a nod to
    "The Hitchhiker's Guide to the Galaxy").

    Parameters
    ----------
    X : pd.DataFrame
        Feature matrix (all columns except the target).
    y : pd.Series
        Target vector (house prices).
    test_size : float, optional
        Fraction of data to reserve for testing (default: 0.2 = 20%).
    random_state : int, optional
        Seed for the random number generator (default: 42).

    Returns
    -------
    X_train : pd.DataFrame
        Training features (80% of data).
    X_test : pd.DataFrame
        Testing features (20% of data).
    y_train : pd.Series
        Training target values.
    y_test : pd.Series
        Testing target values.
    """
    print("=" * 70)
    print("STEP 4: SPLITTING DATA INTO TRAIN / TEST SETS")
    print("=" * 70)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
    )

    print(f"  Total samples  : {len(X):>8,}")
    print(f"  Training set   : {len(X_train):>8,} ({100 * len(X_train) / len(X):.0f}%)")
    print(f"  Testing set    : {len(X_test):>8,} ({100 * len(X_test) / len(X):.0f}%)")
    print(f"  Feature columns: {X_train.shape[1]:>8,}")
    print()

    # Quick sanity check: ensure no data was lost in the split
    assert len(X_train) + len(X_test) == len(X), "Data split error: rows don't add up!"

    return X_train, X_test, y_train, y_test


def build_pipeline(preprocessor, model):
    """
    Combine the preprocessor and a model into a single sklearn Pipeline.

    A Pipeline ensures that:
    1. During training (fit): The preprocessor learns statistics (means, stds,
       category lists) from the TRAINING data only, then the model trains on
       the transformed features.
    2. During prediction (predict): The SAME learned transformations are applied
       to new data before the model makes predictions.

    This prevents "data leakage" — accidentally using test data statistics
    during training, which would give overly optimistic performance estimates.

    Parameters
    ----------
    preprocessor : sklearn.compose.ColumnTransformer
        The unfitted preprocessing transformer (from preprocess_data()).
    model : sklearn estimator
        Any scikit-learn compatible model (e.g., LinearRegression(),
        RandomForestRegressor(), XGBRegressor()).

    Returns
    -------
    sklearn.pipeline.Pipeline
        A complete pipeline: raw DataFrame → preprocessed features → predictions.

    Example
    -------
    >>> from sklearn.linear_model import LinearRegression
    >>> pipeline = build_pipeline(preprocessor, LinearRegression())
    >>> pipeline.fit(X_train, y_train)
    >>> predictions = pipeline.predict(X_test)
    """
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),  # Step 1: Clean and transform features
        ("model", model),                # Step 2: Train/predict with the ML model
    ])

    print(f"  ✅ Pipeline built with model: {type(model).__name__}")
    print(f"     Steps: {[name for name, _ in pipeline.steps]}")

    return pipeline


def main():
    """
    Execute the complete preprocessing pipeline end-to-end.

    This function orchestrates all the steps:
    1. Load the raw CSV data
    2. Explore and understand the data
    3. Build the preprocessing pipeline
    4. Split into train/test sets
    5. Print a final summary

    Returns
    -------
    dict
        A dictionary containing all key objects for downstream use:
        - 'df': The original DataFrame
        - 'X_train', 'X_test': Feature DataFrames
        - 'y_train', 'y_test': Target Series
        - 'preprocessor': The unfitted ColumnTransformer
    """
    print("\n" + "█" * 70)
    print("  INDIAN HOUSE PRICE PREDICTION — DATA PREPROCESSING PIPELINE")
    print("█" * 70 + "\n")

    # Step 1: Load the dataset from CSV
    df = load_data()

    # Step 2: Explore the data — understand what we're working with
    explore_data(df)

    # Step 3: Build the preprocessing pipeline (separate X and y, create transformer)
    X, y, preprocessor = preprocess_data(df)

    # Step 4: Split into training and testing sets
    X_train, X_test, y_train, y_test = split_data(X, y)

    # --- Final Summary ---
    print("=" * 70)
    print("PIPELINE SUMMARY")
    print("=" * 70)
    print(f"  Original dataset      : {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"  Feature columns       : {X.shape[1]}")
    print(f"  Training samples      : {X_train.shape[0]:,}")
    print(f"  Testing samples       : {X_test.shape[0]:,}")
    print(f"  Target (Price) range  : ₹{y.min():,.0f} — ₹{y.max():,.0f}")
    print(f"  Preprocessor type     : {type(preprocessor).__name__}")
    print(f"  Preprocessor status   : UNFITTED (will fit on training data only)")
    print()
    print("  ✅ Data preprocessing pipeline is ready!")
    print("     Next step: Import these objects in your model training script.")
    print("     Example:")
    print("       from data_preprocessing import main as prep_main")
    print("       result = prep_main()")
    print("       X_train = result['X_train']")
    print()

    # Return everything so other scripts can import and use these objects
    return {
        "df": df,
        "X": X,
        "y": y,
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "preprocessor": preprocessor,
    }


# ---------------------------------------------------------------------------
# Entry point: Run the pipeline when this script is executed directly
# ---------------------------------------------------------------------------
# The if __name__ == "__main__" guard ensures that main() only runs when you
# execute this file directly (python data_preprocessing.py), NOT when you
# import functions from it in another script (import data_preprocessing).
if __name__ == "__main__":
    result = main()
