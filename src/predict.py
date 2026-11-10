"""
predict.py - Prediction Module for Indian House Price Prediction
=================================================================
This module provides functions to:
  1. Load the trained model pipeline
  2. Make price predictions for new property data
  3. Format predicted prices in the Indian numbering system
  4. Retrieve valid input options from the training dataset

Author : Senior ML Engineer
Project: Indian House Price Prediction
"""

import os
import sys
import joblib
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Path Configuration
# ---------------------------------------------------------------------------
# Determine the project root directory (one level up from src/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Standard paths used across the project
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "house_price_model.pkl")

# Check possible data locations
_candidate_paths = [
    os.path.join(PROJECT_ROOT, "data", "house_prices.csv"),
    os.path.join(PROJECT_ROOT, "data", "train.csv"),
    os.path.join(PROJECT_ROOT, "data", "raw", "indian_house_prices.csv"),
]
DATA_PATH = next((p for p in _candidate_paths if os.path.exists(p)), _candidate_paths[0])

# The exact column order expected by the trained pipeline
FEATURE_COLUMNS = [
    "City",
    "Locality",
    "Property_Type",
    "BHK",
    "Bathrooms",
    "Super_Built_Up_Area_sqft",
    "Carpet_Area_sqft",
    "Property_Age_years",
    "Furnishing_Status",
    "Floor_No",
    "Total_Floors",
    "Parking",
    "Lift",
    "Gated_Community",
]


# ---------------------------------------------------------------------------
# 1. Model Loading
# ---------------------------------------------------------------------------
def load_model(model_path: str = MODEL_PATH):
    """
    Load the trained scikit-learn pipeline from a joblib file.

    Parameters
    ----------
    model_path : str
        Absolute or relative path to the saved .pkl model file.

    Returns
    -------
    sklearn.pipeline.Pipeline
        The loaded model pipeline ready for prediction.

    Raises
    ------
    FileNotFoundError
        If the model file does not exist at the specified path.
    RuntimeError
        If the model file cannot be loaded (corrupt / incompatible).
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model file not found at '{model_path}'. "
            "Please train the model first by running src/train.py."
        )

    try:
        model = joblib.load(model_path)
        print(f"[INFO] Model loaded successfully from '{model_path}'")
        return model
    except Exception as e:
        raise RuntimeError(
            f"Failed to load model from '{model_path}': {e}"
        ) from e


# ---------------------------------------------------------------------------
# 2. Price Prediction
# ---------------------------------------------------------------------------
def predict_price(model, input_data: dict) -> float:
    """
    Predict the price of a property given its features.

    Parameters
    ----------
    model : sklearn.pipeline.Pipeline
        The trained model pipeline (preprocessor + estimator).
    input_data : dict
        Dictionary mapping feature names to their values.
        Example::

            {
                "City": "Mumbai",
                "Locality": "Andheri West",
                "Property_Type": "Apartment",
                "BHK": 2,
                "Bathrooms": 2,
                "Super_Built_Up_Area_sqft": 1100,
                "Carpet_Area_sqft": 850,
                "Property_Age_years": 5,
                "Furnishing_Status": "Semi-Furnished",
                "Floor_No": 7,
                "Total_Floors": 20,
                "Parking": 1,
                "Lift": 1,
                "Gated_Community": 1,
            }

    Returns
    -------
    float
        Predicted house price in INR.

    Raises
    ------
    ValueError
        If required features are missing from *input_data*.
    """
    # --- Validate that all required features are present ---
    missing = [col for col in FEATURE_COLUMNS if col not in input_data]
    if missing:
        raise ValueError(
            f"Missing required feature(s): {missing}. "
            f"Expected features: {FEATURE_COLUMNS}"
        )

    # --- Build a single-row DataFrame with the correct column order ---
    input_df = pd.DataFrame([input_data], columns=FEATURE_COLUMNS)

    # --- Run prediction through the pipeline ---
    prediction = model.predict(input_df)

    # The pipeline may return a log-transformed price; handle both cases.
    predicted_price = float(prediction[0])

    # If the model was trained on log(Price), the predicted value will be
    # small (e.g. < 50). Un-transform it back to INR.
    if predicted_price < 1000:
        predicted_price = float(np.expm1(predicted_price))

    return predicted_price


# ---------------------------------------------------------------------------
# 3. Indian Price Formatting
# ---------------------------------------------------------------------------
def format_indian_price(price) -> dict:
    """
    Format a price (in INR) using the Indian numbering system.

    Indian grouping rules:
        * The last three digits are grouped together.
        * Every subsequent group contains two digits.
        * Example: 1,23,45,678

    Parameters
    ----------
    price : float | int
        Raw price value in INR.

    Returns
    -------
    dict
        A dictionary with keys:
        - ``'raw'``   : the original numeric value
        - ``'inr'``   : formatted string like ``"₹1,23,45,678"``
        - ``'lakhs'`` : string like ``"123.46 Lakhs"``
        - ``'crores'``: string like ``"1.23 Crores"`` (present only if >= 1 Cr)
    """
    price = float(price)

    # --- Indian-style comma formatting ---
    inr_formatted = _indian_comma_format(abs(price))
    if price < 0:
        inr_formatted = "-" + inr_formatted
    inr_str = f"₹{inr_formatted}"

    # --- Lakhs representation (1 Lakh = 1,00,000) ---
    lakhs_value = price / 1_00_000
    lakhs_str = f"{lakhs_value:,.2f} Lakhs"

    # --- Build result dictionary ---
    result = {
        "raw": price,
        "inr": inr_str,
        "lakhs": lakhs_str,
    }

    # --- Crores representation (1 Crore = 1,00,00,000) ---
    if abs(price) >= 1_00_00_000:
        crores_value = price / 1_00_00_000
        result["crores"] = f"{crores_value:,.2f} Crores"

    return result


def _indian_comma_format(number) -> str:
    """
    Internal helper: format an integer/float with Indian-style commas.

    Steps:
        1. Separate the integer and decimal parts.
        2. Group the last 3 digits of the integer part.
        3. Group the remaining digits in pairs from right to left.
        4. Rejoin with commas.

    Examples
    --------
    >>> _indian_comma_format(4500000)
    '45,00,000'
    >>> _indian_comma_format(123456789)
    '12,34,56,789'
    >>> _indian_comma_format(1500)
    '1,500'
    >>> _indian_comma_format(999)
    '999'
    """
    # Round to nearest integer for display
    number = int(round(number))
    num_str = str(number)

    # If <= 3 digits, no comma needed
    if len(num_str) <= 3:
        return num_str

    # Split into the last 3 digits and the rest
    last_three = num_str[-3:]
    remaining = num_str[:-3]

    # Group the remaining digits in pairs from the right
    groups = []
    while len(remaining) > 2:
        groups.append(remaining[-2:])
        remaining = remaining[:-2]
    if remaining:
        groups.append(remaining)

    # Reverse to restore left-to-right order and join
    groups.reverse()
    return ",".join(groups) + "," + last_three


# ---------------------------------------------------------------------------
# 4. Valid Input Options
# ---------------------------------------------------------------------------
def get_valid_options(data_path: str = DATA_PATH) -> dict:
    """
    Read the training dataset and extract valid values for each input field.

    This is useful for building UIs / CLI prompts that constrain user input
    to values the model has seen during training.

    Parameters
    ----------
    data_path : str
        Path to the raw training CSV file.

    Returns
    -------
    dict
        Dictionary with the following keys:

        - ``cities``             : sorted list of unique city names
        - ``localities``         : dict mapping city → sorted list of localities
        - ``property_types``     : sorted list of property type strings
        - ``furnishing_statuses``: sorted list of furnishing status strings
        - ``bhk_range``          : (min, max) tuple for BHK
        - ``bathroom_range``     : (min, max) tuple for Bathrooms
        - ``area_range``         : (min, max) tuple for Super_Built_Up_Area_sqft
        - ``floor_range``        : (min, max) tuple for Floor_No
        - ``parking_range``      : (min, max) tuple for Parking

    Raises
    ------
    FileNotFoundError
        If the training CSV does not exist at *data_path*.
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(
            f"Training data not found at '{data_path}'. "
            "Please ensure the dataset is placed in data/raw/."
        )

    df = pd.read_csv(data_path)

    # --- Categorical options ---
    cities = sorted(df["City"].dropna().unique().tolist())

    # Build a mapping of city → sorted list of its localities
    localities = {}
    for city in cities:
        city_localities = (
            df.loc[df["City"] == city, "Locality"]
            .dropna()
            .unique()
            .tolist()
        )
        localities[city] = sorted(city_localities)

    property_types = sorted(df["Property_Type"].dropna().unique().tolist())
    furnishing_statuses = sorted(
        df["Furnishing_Status"].dropna().unique().tolist()
    )

    # --- Numeric ranges ---
    bhk_range = (int(df["BHK"].min()), int(df["BHK"].max()))
    bathroom_range = (int(df["Bathrooms"].min()), int(df["Bathrooms"].max()))
    area_range = (
        int(df["Super_Built_Up_Area_sqft"].min()),
        int(df["Super_Built_Up_Area_sqft"].max()),
    )
    floor_range = (int(df["Floor_No"].min()), int(df["Floor_No"].max()))
    parking_range = (int(df["Parking"].min()), int(df["Parking"].max()))

    options = {
        "cities": cities,
        "localities": localities,
        "property_types": property_types,
        "furnishing_statuses": furnishing_statuses,
        "bhk_range": bhk_range,
        "bathroom_range": bathroom_range,
        "area_range": area_range,
        "floor_range": floor_range,
        "parking_range": parking_range,
    }

    print(f"[INFO] Loaded valid options from '{data_path}'")
    print(f"       Cities: {len(cities)}, Property Types: {len(property_types)}")
    return options


# ---------------------------------------------------------------------------
# 5. Main – Demonstration
# ---------------------------------------------------------------------------
def main():
    """
    Demonstrate the full prediction workflow:
        1. Load the trained model
        2. Prepare a sample property input
        3. Predict the price
        4. Format and display the result
    """
    print("=" * 65)
    print("  Indian House Price Prediction – Inference Demo")
    print("=" * 65)

    # Step 1: Load the trained model pipeline
    try:
        model = load_model()
    except (FileNotFoundError, RuntimeError) as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    # Step 2: Define a sample property for prediction
    sample_input = {
        "City": "Mumbai",
        "Locality": "Andheri West",
        "Property_Type": "Apartment",
        "BHK": 2,
        "Bathrooms": 2,
        "Super_Built_Up_Area_sqft": 1100,
        "Carpet_Area_sqft": 850,
        "Property_Age_years": 5,
        "Furnishing_Status": "Semi-Furnished",
        "Floor_No": 7,
        "Total_Floors": 20,
        "Parking": 1,
        "Lift": 1,
        "Gated_Community": 1,
    }

    print("\n📋 Sample Property Details:")
    print("-" * 40)
    for key, value in sample_input.items():
        print(f"  {key:<28s}: {value}")

    # Step 3: Predict the price
    try:
        predicted_price = predict_price(model, sample_input)
    except ValueError as e:
        print(f"[ERROR] Prediction failed: {e}")
        sys.exit(1)

    # Step 4: Format the price in Indian numbering system
    formatted = format_indian_price(predicted_price)

    print("\n💰 Predicted Price:")
    print("-" * 40)
    print(f"  INR (formatted) : {formatted['inr']}")
    print(f"  In Lakhs        : {formatted['lakhs']}")
    if "crores" in formatted:
        print(f"  In Crores       : {formatted['crores']}")
    print(f"  Raw value       : {formatted['raw']:,.2f}")

    # Step 5: Show valid options (optional, for reference)
    print("\n📊 Valid Input Ranges:")
    print("-" * 40)
    try:
        options = get_valid_options()
        print(f"  Cities          : {', '.join(options['cities'][:5])}...")
        print(f"  Property Types  : {', '.join(options['property_types'])}")
        print(f"  BHK Range       : {options['bhk_range'][0]} – {options['bhk_range'][1]}")
        print(f"  Bathroom Range  : {options['bathroom_range'][0]} – {options['bathroom_range'][1]}")
        print(f"  Area Range      : {options['area_range'][0]:,} – {options['area_range'][1]:,} sqft")
        print(f"  Floor Range     : {options['floor_range'][0]} – {options['floor_range'][1]}")
        print(f"  Parking Range   : {options['parking_range'][0]} – {options['parking_range'][1]}")
        print(f"  Furnishing      : {', '.join(options['furnishing_statuses'])}")
    except FileNotFoundError as e:
        print(f"  [WARN] {e}")

    print("\n" + "=" * 65)
    print("  Prediction complete.")
    print("=" * 65)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
