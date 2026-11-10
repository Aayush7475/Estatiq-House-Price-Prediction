"""
ESTATIQ Backend API — Indian House Price Prediction System
===========================================================
Production-ready FastAPI backend serving the Scikit-learn Random Forest
housing valuation pipeline.

Features:
- GET /health        : Health check & model status
- GET /model-info    : Model architecture, metrics, and supported input spaces
- POST /predict      : Real-time property valuation inference
"""

import os
import sys
import json
import joblib
import pandas as pd
import numpy as np
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# -----------------------------------------------------------------------------
# Configuration & File Path Resolution
# -----------------------------------------------------------------------------
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_CANDIDATES = [
    os.path.join(BACKEND_DIR, "models", "house_price_model.pkl"),
    os.path.join(os.path.dirname(BACKEND_DIR), "models", "house_price_model.pkl"),
]
MODEL_PATH = next((p for p in MODEL_CANDIDATES if os.path.exists(p)), MODEL_CANDIDATES[0])

METRICS_CANDIDATES = [
    os.path.join(BACKEND_DIR, "models", "evaluation_metrics.json"),
    os.path.join(os.path.dirname(BACKEND_DIR), "models", "evaluation_metrics.json"),
]
METRICS_PATH = next((p for p in METRICS_CANDIDATES if os.path.exists(p)), METRICS_CANDIDATES[0])

DATA_CANDIDATES = [
    os.path.join(BACKEND_DIR, "data", "house_prices.csv"),
    os.path.join(os.path.dirname(BACKEND_DIR), "data", "house_prices.csv"),
]
DATA_PATH = next((p for p in DATA_CANDIDATES if os.path.exists(p)), DATA_CANDIDATES[0])

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

# -----------------------------------------------------------------------------
# Model & Metadata Loading
# -----------------------------------------------------------------------------
ml_model = None
try:
    if os.path.exists(MODEL_PATH):
        ml_model = joblib.load(MODEL_PATH)
        print(f"[INFO] Loaded ML Model successfully from '{MODEL_PATH}'")
    else:
        print(f"[WARN] Model file not found at '{MODEL_PATH}'")
except Exception as e:
    print(f"[ERROR] Failed to load model: {e}")

# Load evaluation metrics
evaluation_metrics: Dict[str, Any] = {}
if os.path.exists(METRICS_PATH):
    try:
        with open(METRICS_PATH, "r") as f:
            evaluation_metrics = json.load(f)
    except Exception as e:
        print(f"[WARN] Could not parse metrics file: {e}")

# Load options from dataset
cached_options: Dict[str, Any] = {
    "cities": ["Ahmedabad", "Bangalore", "Chennai", "Delhi", "Hyderabad", "Jaipur", "Kolkata", "Lucknow", "Mumbai", "Pune"],
    "localities": {},
    "property_types": ["Apartment", "Builder Floor", "Independent House", "Villa"],
    "furnishing_statuses": ["Furnished", "Semi-Furnished", "Unfurnished"],
    "bhk_range": [1, 5],
    "bathroom_range": [1, 6],
    "area_range": [400, 4000],
    "floor_range": [0, 30],
    "parking_range": [0, 3],
}

if os.path.exists(DATA_PATH):
    try:
        df_sample = pd.read_csv(DATA_PATH)
        cities_list = sorted(df_sample["City"].dropna().unique().tolist())
        loc_map = {}
        for c in cities_list:
            loc_map[c] = sorted(df_sample[df_sample["City"] == c]["Locality"].dropna().unique().tolist())
        cached_options["cities"] = cities_list
        cached_options["localities"] = loc_map
        cached_options["property_types"] = sorted(df_sample["Property_Type"].dropna().unique().tolist())
        cached_options["furnishing_statuses"] = sorted(df_sample["Furnishing_Status"].dropna().unique().tolist())
        cached_options["bhk_range"] = [int(df_sample["BHK"].min()), int(df_sample["BHK"].max())]
        cached_options["bathroom_range"] = [int(df_sample["Bathrooms"].min()), int(df_sample["Bathrooms"].max())]
        cached_options["area_range"] = [int(df_sample["Super_Built_Up_Area_sqft"].min()), int(df_sample["Super_Built_Up_Area_sqft"].max())]
        print(f"[INFO] Loaded dynamic options from '{DATA_PATH}'")
    except Exception as e:
        print(f"[WARN] Error reading dataset options: {e}")

# -----------------------------------------------------------------------------
# FastAPI Application & CORS Setup
# -----------------------------------------------------------------------------
app = FastAPI(
    title="ESTATIQ Real Estate Valuation API",
    description="Production-grade AI property valuation engine powered by Scikit-learn regression models.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://aayush-estatiq.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def format_inr_currency(price: float) -> Dict[str, Any]:
    """Format price using the Indian numbering system."""
    rounded_price = round(price)
    s = str(abs(rounded_price))
    if len(s) <= 3:
        formatted_num = s
    else:
        last_three = s[-3:]
        remaining = s[:-3]
        groups = []
        while len(remaining) > 2:
            groups.append(remaining[-2:])
            remaining = remaining[:-2]
        if remaining:
            groups.append(remaining)
        groups.reverse()
        formatted_num = ",".join(groups) + "," + last_three

    inr_str = f"₹{formatted_num}"
    lakhs_str = f"{price / 100000:.2f} Lakhs"
    
    result = {
        "raw": float(price),
        "inr": inr_str,
        "lakhs": lakhs_str,
        "price_in_lakhs": round(price / 100000, 2),
    }

    if price >= 10000000:
        result["crores"] = f"{price / 10000000:.2f} Crores"
        result["price_in_crores"] = round(price / 10000000, 2)

    return result

# -----------------------------------------------------------------------------
# Pydantic Schemas
# -----------------------------------------------------------------------------
class PropertyPredictionInput(BaseModel):
    city: str = Field(..., description="Metropolitan city name (e.g. Mumbai, Bangalore)")
    locality: str = Field(..., description="Locality / neighborhood within the city")
    property_type: str = Field(..., description="Type of property: Apartment, Independent House, Villa, Builder Floor")
    bhk: int = Field(..., ge=1, le=10, description="Number of bedrooms (BHK)")
    bathrooms: int = Field(..., ge=1, le=10, description="Number of bathrooms")
    super_builtup_area: float = Field(..., gt=0, le=20000, description="Super Built-Up Area in square feet")
    carpet_area: float = Field(..., gt=0, le=20000, description="Carpet Area in square feet")
    property_age: int = Field(0, ge=0, le=100, description="Age of the property in years")
    furnishing_status: str = Field(..., description="Furnished, Semi-Furnished, or Unfurnished")
    floor_no: int = Field(0, ge=0, le=100, description="Floor number of the unit (0 for ground)")
    total_floors: int = Field(1, ge=1, le=100, description="Total floors in the building")
    parking: int = Field(1, ge=0, le=10, description="Number of dedicated parking slots")
    lift: int = Field(1, ge=0, le=1, description="1 if lift is available, 0 otherwise")
    gated_community: int = Field(1, ge=0, le=1, description="1 if in a gated complex with security, 0 otherwise")

    class Config:
        json_schema_extra = {
            "example": {
                "city": "Mumbai",
                "locality": "Andheri West",
                "property_type": "Apartment",
                "bhk": 2,
                "bathrooms": 2,
                "super_builtup_area": 1100,
                "carpet_area": 850,
                "property_age": 5,
                "furnishing_status": "Semi-Furnished",
                "floor_no": 7,
                "total_floors": 20,
                "parking": 1,
                "lift": 1,
                "gated_community": 1
            }
        }

class ValuationResponse(BaseModel):
    success: bool
    predicted_price: float
    formatted_inr: str
    price_lakhs: str
    price_crores: Optional[str] = None
    price_per_sqft: float
    property_summary: Dict[str, Any]
    model_name: str
    timestamp: str

# -----------------------------------------------------------------------------
# Endpoints
# -----------------------------------------------------------------------------
@app.get("/", tags=["Root"])
def root():
    return {
        "platform": "ESTATIQ Real Estate Intelligence API",
        "version": "2.0.0",
        "status": "online",
        "docs_url": "/docs",
        "health_check": "/health",
        "model_info": "/model-info",
        "predict_endpoint": "/predict",
    }

@app.get("/health", tags=["Monitoring"])
def health_check():
    """Verify backend health and model readiness."""
    return {
        "status": "healthy",
        "model_loaded": ml_model is not None,
        "model_type": type(ml_model.named_steps["model"]).__name__ if ml_model and hasattr(ml_model, "named_steps") else "Unknown",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "environment": "production",
    }

@app.get("/model-info", tags=["Model Telemetry"])
def model_info():
    """Return model metadata, features, options, and validation metrics."""
    return {
        "model_name": "Random Forest Regressor (ESTATIQ Production Pipeline)",
        "framework": "Scikit-learn with ColumnTransformer & Pipeline",
        "status": "ready" if ml_model is not None else "model_not_loaded",
        "features_expected": FEATURE_COLUMNS,
        "evaluation_metrics": evaluation_metrics,
        "supported_options": cached_options,
    }

@app.post("/predict", response_model=ValuationResponse, tags=["Inference"])
def predict(payload: PropertyPredictionInput):
    """
    Compute estimated property valuation using the trained Random Forest model.
    """
    if ml_model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Machine learning model is not loaded on the server. Please check /health.",
        )

    try:
        # Build DataFrame with exact feature names and order expected by ColumnTransformer
        input_dict = {
            "City": [payload.city],
            "Locality": [payload.locality],
            "Property_Type": [payload.property_type],
            "BHK": [payload.bhk],
            "Bathrooms": [payload.bathrooms],
            "Super_Built_Up_Area_sqft": [payload.super_builtup_area],
            "Carpet_Area_sqft": [payload.carpet_area],
            "Property_Age_years": [payload.property_age],
            "Furnishing_Status": [payload.furnishing_status],
            "Floor_No": [payload.floor_no],
            "Total_Floors": [payload.total_floors],
            "Parking": [payload.parking],
            "Lift": [payload.lift],
            "Gated_Community": [payload.gated_community],
        }

        df_input = pd.DataFrame(input_dict)
        
        # Execute pipeline prediction
        raw_pred = ml_model.predict(df_input)[0]
        
        # Guard against anomalous negative estimates
        predicted_price = float(max(raw_pred, 500000.0))
        
        # Format currency
        fmt = format_inr_currency(predicted_price)
        price_per_sqft = round(predicted_price / payload.super_builtup_area, 2)

        return ValuationResponse(
            success=True,
            predicted_price=predicted_price,
            formatted_inr=fmt["inr"],
            price_lakhs=fmt["lakhs"],
            price_crores=fmt.get("crores"),
            price_per_sqft=price_per_sqft,
            property_summary={
                "city": payload.city,
                "locality": payload.locality,
                "property_type": payload.property_type,
                "bhk": payload.bhk,
                "bathrooms": payload.bathrooms,
                "super_builtup_area": payload.super_builtup_area,
                "carpet_area": payload.carpet_area,
                "property_age": payload.property_age,
                "furnishing_status": payload.furnishing_status,
                "floor_no": payload.floor_no,
                "total_floors": payload.total_floors,
                "parking": payload.parking,
                "lift": bool(payload.lift),
                "gated_community": bool(payload.gated_community),
            },
            model_name="RandomForestRegressor (100 Trees Ensemble)",
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction inference error: {str(e)}",
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

