"""
TEST SUITE FOR INDIAN HOUSE PRICE PREDICTION SYSTEM
====================================================
Comprehensive tests verifying all components of the ML project:
- File existence
- Data integrity
- Model loading and inference
- Multiple property configurations
- Unseen category handling
- Missing value imputation
- Indian currency formatting
- Evaluation metrics consistency
"""

import os
import sys
import json
import numpy as np
import pandas as pd

# Add project root and src to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))

from predict import load_model, predict_price, format_indian_price, get_valid_options
from data_preprocessing import load_data, preprocess_data, split_data


def test_01_required_files_exist():
    """Verify that all core files and folders exist in the workspace."""
    required_paths = [
        "data/house_prices.csv",
        "data/train.csv",
        "models/house_price_model.pkl",
        "models/evaluation_metrics.json",
        "src/generate_dataset.py",
        "src/data_preprocessing.py",
        "src/eda.py",
        "src/train_model.py",
        "src/predict.py",
        "outputs/charts/model_comparison.png",
        "outputs/charts/price_distribution.png",
        "outputs/charts/avg_price_by_city.png",
        "outputs/charts/price_vs_area.png",
        "outputs/charts/bhk_vs_price.png",
        "outputs/charts/property_type_comparison.png",
        "outputs/charts/correlation_heatmap.png",
        "outputs/charts/numerical_distributions.png",
        "outputs/charts/furnishing_vs_price.png",
        "app.py",
        "backend/main.py",
        "backend/models/house_price_model.pkl",
        "backend/requirements.txt",
        "frontend/package.json",
        "frontend/src/app/page.tsx",
        "requirements.txt",
        ".gitignore",
    ]
    for rel_path in required_paths:
        full_path = os.path.join(PROJECT_ROOT, rel_path)
        assert os.path.exists(full_path), f"Missing required file: {rel_path}"
    print("✅ Test 1 Passed: All required project files exist.")


def test_02_dataset_integrity():
    """Verify dataset columns, non-emptiness, and shape."""
    df = load_data()
    assert len(df) == 5000, f"Expected 5000 rows, found {len(df)}"
    
    expected_cols = [
        "City", "Locality", "Property_Type", "BHK", "Bathrooms",
        "Super_Built_Up_Area_sqft", "Carpet_Area_sqft", "Property_Age_years",
        "Furnishing_Status", "Floor_No", "Total_Floors", "Parking",
        "Lift", "Gated_Community", "Price"
    ]
    for col in expected_cols:
        assert col in df.columns, f"Missing column: {col}"
    
    assert df["Price"].min() > 0, "Prices must be positive"
    assert df["Super_Built_Up_Area_sqft"].min() >= 300, "Area must be realistic"
    print("✅ Test 2 Passed: Dataset integrity verified.")


def test_03_model_loading_and_pipeline():
    """Verify that the model loads and contains preprocessor and model steps."""
    model = load_model()
    assert model is not None
    assert hasattr(model, "predict"), "Model must have predict method"
    assert "preprocessor" in model.named_steps, "Pipeline must have preprocessor step"
    assert "model" in model.named_steps, "Pipeline must have model step"
    print("✅ Test 3 Passed: Model loaded and pipeline verified.")


def test_04_prediction_multiple_configurations():
    """Test model prediction across different realistic property configurations."""
    model = load_model()
    
    test_cases = [
        {
            "name": "Budget 1 BHK Apartment in Kolkata",
            "data": {
                "City": "Kolkata",
                "Locality": "Dum Dum",
                "Property_Type": "Apartment",
                "BHK": 1,
                "Bathrooms": 1,
                "Super_Built_Up_Area_sqft": 500,
                "Carpet_Area_sqft": 360,
                "Property_Age_years": 10,
                "Furnishing_Status": "Unfurnished",
                "Floor_No": 2,
                "Total_Floors": 5,
                "Parking": 0,
                "Lift": 0,
                "Gated_Community": 0
            },
            "min_expected": 1_000_000,
            "max_expected": 15_000_000
        },
        {
            "name": "Mid-tier 2 BHK Apartment in Bangalore",
            "data": {
                "City": "Bangalore",
                "Locality": "Whitefield",
                "Property_Type": "Apartment",
                "BHK": 2,
                "Bathrooms": 2,
                "Super_Built_Up_Area_sqft": 1050,
                "Carpet_Area_sqft": 780,
                "Property_Age_years": 3,
                "Furnishing_Status": "Semi-Furnished",
                "Floor_No": 6,
                "Total_Floors": 14,
                "Parking": 1,
                "Lift": 1,
                "Gated_Community": 1
            },
            "min_expected": 4_000_000,
            "max_expected": 30_000_000
        },
        {
            "name": "Luxury 4 BHK Villa in South Mumbai",
            "data": {
                "City": "Mumbai",
                "Locality": "Bandra",
                "Property_Type": "Villa",
                "BHK": 4,
                "Bathrooms": 5,
                "Super_Built_Up_Area_sqft": 3200,
                "Carpet_Area_sqft": 2400,
                "Property_Age_years": 1,
                "Furnishing_Status": "Furnished",
                "Floor_No": 0,
                "Total_Floors": 2,
                "Parking": 3,
                "Lift": 1,
                "Gated_Community": 1
            },
            "min_expected": 30_000_000,
            "max_expected": 200_000_000
        }
    ]
    
    for tc in test_cases:
        pred = predict_price(model, tc["data"])
        assert isinstance(pred, (int, float, np.floating)), f"Prediction must be numeric for {tc['name']}"
        assert pred > 0, f"Predicted price must be positive for {tc['name']}"
        assert tc["min_expected"] <= pred <= tc["max_expected"], (
            f"Prediction ₹{pred:,.0f} out of expected range "
            f"[₹{tc['min_expected']:,.0f}, ₹{tc['max_expected']:,.0f}] for {tc['name']}"
        )
        print(f"   ✓ {tc['name']}: ₹{pred:,.0f}")
        
    print("✅ Test 4 Passed: Multiple property configurations tested successfully.")


def test_05_unseen_categorical_handling():
    """Verify that unseen categorical values do not crash the pipeline."""
    model = load_model()
    unseen_input = {
        "City": "Goa",                     # Unseen city
        "Locality": "Panaji Beach Road",    # Unseen locality
        "Property_Type": "Penthouse",       # Unseen property type
        "BHK": 3,
        "Bathrooms": 3,
        "Super_Built_Up_Area_sqft": 1500,
        "Carpet_Area_sqft": 1100,
        "Property_Age_years": 2,
        "Furnishing_Status": "Ultra-Luxury", # Unseen furnishing
        "Floor_No": 10,
        "Total_Floors": 15,
        "Parking": 2,
        "Lift": 1,
        "Gated_Community": 1
    }
    pred = predict_price(model, unseen_input)
    assert pred > 0, "Model should produce a positive estimate even with unseen categories"
    print(f"✅ Test 5 Passed: Unseen categories handled gracefully (Prediction: ₹{pred:,.0f}).")


def test_06_missing_values_handling():
    """Verify that inputs with missing numerical/categorical values are handled via pipeline imputer."""
    model = load_model()
    missing_input = {
        "City": "Bangalore",
        "Locality": None,                  # Missing categorical
        "Property_Type": "Apartment",
        "BHK": 2,
        "Bathrooms": np.nan,               # Missing numerical
        "Super_Built_Up_Area_sqft": 1000,
        "Carpet_Area_sqft": None,          # Missing numerical
        "Property_Age_years": 5,
        "Furnishing_Status": "Furnished",
        "Floor_No": 3,
        "Total_Floors": 10,
        "Parking": 1,
        "Lift": 1,
        "Gated_Community": 1
    }
    pred = predict_price(model, missing_input)
    assert pred > 0, "Model should handle missing values through SimpleImputer"
    print(f"✅ Test 6 Passed: Missing values imputed successfully (Prediction: ₹{pred:,.0f}).")


def test_07_currency_formatting():
    """Verify Indian numbering format (Lakhs, Crores, commas)."""
    # 50 Lakhs
    fmt_50l = format_indian_price(5000000)
    assert "₹50,00,000" in fmt_50l["inr"]
    assert "50.00 Lakhs" in fmt_50l["lakhs"]
    
    # 1.5 Crores
    fmt_1_5cr = format_indian_price(15000000)
    assert "₹1,50,00,000" in fmt_1_5cr["inr"]
    assert "1.50 Crores" in fmt_1_5cr.get("crores", "")
    
    # 75,000 (below 1 lakh)
    fmt_75k = format_indian_price(75000)
    assert "₹75,000" in fmt_75k["inr"]
    
    print("✅ Test 7 Passed: Indian currency formatting verified.")


def test_08_evaluation_metrics_consistency():
    """Verify evaluation_metrics.json has all required fields and valid numbers."""
    metrics_path = os.path.join(PROJECT_ROOT, "models", "evaluation_metrics.json")
    with open(metrics_path, "r") as f:
        metrics = json.load(f)
    
    assert "linear_regression" in metrics
    assert "random_forest" in metrics
    assert "best_model" in metrics
    assert "best_model_r2" in metrics
    
    for model_name in ["linear_regression", "random_forest"]:
        m = metrics[model_name]
        for key in ["mae", "mse", "rmse", "r2", "train_r2"]:
            assert key in m, f"Missing metric {key} in {model_name}"
            assert isinstance(m[key], (int, float)), f"Metric {key} must be numeric"
        
        # Check that RMSE is sqrt(MSE) approximately
        assert np.isclose(np.sqrt(m["mse"]), m["rmse"], rtol=0.01), (
            f"RMSE should match sqrt(MSE) for {model_name}"
        )
        
        # R2 score must be <= 1.0
        assert m["r2"] <= 1.0, f"R² score cannot exceed 1.0"
        assert m["train_r2"] <= 1.0, f"Train R² score cannot exceed 1.0"
    
    print("✅ Test 8 Passed: Evaluation metrics are consistent and valid.")


def test_09_fastapi_backend_integration():
    """Verify that the FastAPI backend loads the ML model and serves predictions."""
    from backend.main import health_check, model_info, predict, PropertyPredictionInput
    
    health = health_check()
    assert health["status"] == "healthy", "FastAPI health check failed"
    assert health["model_loaded"] is True, "FastAPI model must be loaded"

    info = model_info()
    assert info["status"] == "ready", "Model status must be ready"
    assert len(info["features_expected"]) == 14, "Expected 14 input features"

    sample = PropertyPredictionInput(
        city="Mumbai",
        locality="Andheri West",
        property_type="Apartment",
        bhk=2,
        bathrooms=2,
        super_builtup_area=1100,
        carpet_area=850,
        property_age=5,
        furnishing_status="Semi-Furnished",
        floor_no=7,
        total_floors=20,
        parking=1,
        lift=1,
        gated_community=1
    )
    res = predict(sample)
    assert res.success is True, "Prediction must be successful"
    assert res.predicted_price > 0, "Predicted price must be positive"
    assert "₹" in res.formatted_inr, "Must format price in INR"
    assert "Lakhs" in res.price_lakhs, "Must format price in Lakhs"
    print("✅ Test 9 Passed: FastAPI backend health and prediction verified.")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING INDIAN HOUSE PRICE PREDICTION TEST SUITE")
    print("=" * 60)
    test_01_required_files_exist()
    test_02_dataset_integrity()
    test_03_model_loading_and_pipeline()
    test_04_prediction_multiple_configurations()
    test_05_unseen_categorical_handling()
    test_06_missing_values_handling()
    test_07_currency_formatting()
    test_08_evaluation_metrics_consistency()
    test_09_fastapi_backend_integration()
    print("=" * 60)
    print("🎉 ALL 9 TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)
