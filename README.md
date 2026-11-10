# 🏛️ ESTATIQ — Indian House Price Prediction System
### AI-Powered Real Estate Valuation & Market Analytics Platform

An end-to-end Machine Learning web application designed to predict residential property prices across major metropolitan and Tier-1/2 Indian cities. Re-engineered with the **ESTATIQ** luxury PropTech SaaS interface (Deep Navy `#101827` and Warm Gold `#D6AD60`), this project implements a complete data science pipeline from data preprocessing and exploratory data analysis to model training, evaluation, and interactive web deployment.

> **Academic Submission:** B.Tech Computer Science & Engineering (Final / Semester Machine Learning Project)  
> **Dataset Status:** Synthetic Dataset (5,000 records, 14 input features, algorithmically modeled after Indian urban real estate market dynamics).

---

## 📌 Table of Contents
- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Technologies Used](#-technologies-used)
- [Project Architecture & Structure](#-project-architecture--structure)
- [Dataset Details & Features](#-dataset-details--features)
- [Machine Learning Pipeline](#-machine-learning-pipeline)
- [Model Evaluation & Comparison](#-model-evaluation--comparison)
- [Installation & Setup](#-installation--setup)
- [Step-by-Step Execution Guide](#-step-by-step-execution-guide)
- [Streamlit Web Interface Overview](#-streamlit-web-interface-overview)
- [Automated Test Suite](#-automated-test-suite)
- [Limitations & Future Scope](#-limitations--future-scope)
- [License](#-license)

---

## 🌟 Project Overview

Estimating fair property prices in India is notoriously difficult due to extreme regional variability, disparity between carpet and super built-up areas, building age depreciation, floor rise premiums, and amenities such as gated security and lifts.

This project delivers:
1. **Automated Machine Learning Regression** capable of predicting property prices in Indian Rupees (₹), formatted in Lakhs and Crores.
2. **A Scikit-Learn Pipeline** that seamlessly handles both numeric scaling and categorical one-hot encoding without data leakage.
3. **Rigorous Comparison** between baseline Linear Regression and ensemble Random Forest Regressor.
4. **An Interactive 5-Page Streamlit Dashboard** featuring real-time price prediction, exploratory market analytics, project documentation, and model telemetry.

---

## ✨ Key Features

- **Multi-City Support:** Covers 10 prominent Indian cities:
  * Mumbai, Delhi, Bangalore, Hyderabad, Chennai, Pune, Kolkata, Ahmedabad, Jaipur, Lucknow.
- **Locality-Level Granularity:** Over 80 distinct localities mapped to corresponding cities.
- **14 Realistic Property Parameters:** Includes BHK, bathrooms, super built-up area, carpet area, age of property, floor details, parking count, lift availability, and gated community security.
- **Zero Data Leakage:** Preprocessing transformations (imputation, scaling, one-hot encoding) are encapsulated in a `ColumnTransformer` fitted exclusively on the 80% training set.
- **Dual Model Benchmarking:** Side-by-side comparison of **Linear Regression** vs. **Random Forest Regressor** using MAE, MSE, RMSE, and $R^2$.
- **Indian Currency Formatter:** Intelligently formats predictions using the Indian numbering system (e.g., `₹1,84,66,000` -> `184.66 Lakhs` / `1.85 Crores`).
- **Robust Inference:** Gracefully handles missing values and unseen categorical variables via `handle_unknown='ignore'`.

---

## 🛠️ Technologies Used

| Category | Library / Tool | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.13 | Core programming language |
| **Data Processing** | Pandas, NumPy | Data ingestion, manipulation, and numerical arrays |
| **Visualization** | Matplotlib, Seaborn, Plotly | Static and interactive charts & dashboards |
| **Machine Learning** | Scikit-Learn | Pipelines, ColumnTransformer, LinearRegression, RandomForest |
| **Model Persistence** | Joblib | Serializing and loading trained pipeline binaries |
| **Web Application** | Streamlit | Responsive multi-page web frontend |
| **Code Verification** | Python Standard Test Harness | End-to-end integration and unit testing |

---

## 📁 Project Architecture & Structure

```
house-price-prediction/
│
├── data/
│   ├── house_prices.csv             # Primary generated synthetic dataset (5,000 rows)
│   └── train.csv                    # Dataset copy for pipeline compatibility
│
├── models/
│   ├── house_price_model.pkl        # Serialized best Scikit-learn Pipeline (Joblib)
│   └── evaluation_metrics.json      # Quantitative benchmark metrics for both models
│
├── src/
│   ├── __init__.py
│   ├── generate_dataset.py          # Synthetic dataset generator script
│   ├── data_preprocessing.py        # Loading, exploration, splitting & preprocessor pipeline
│   ├── eda.py                       # Exploratory Data Analysis & chart generator (8 plots)
│   ├── train_model.py               # Model training, evaluation, comparison & saving
│   └── predict.py                   # Prediction utility, currency formatting & input schema
│
├── outputs/
│   └── charts/                      # Generated visual artifacts
│       ├── avg_price_by_city.png
│       ├── bhk_vs_price.png
│       ├── correlation_heatmap.png
│       ├── furnishing_vs_price.png
│       ├── model_comparison.png
│       ├── numerical_distributions.png
│       ├── price_distribution.png
│       ├── price_vs_area.png
│       └── property_type_comparison.png
│
├── tests/
│   └── test_system.py               # 8 automated integration and regression tests
│
├── app.py                           # Multi-page interactive Streamlit web dashboard
├── requirements.txt                 # Pinned project dependencies
├── README.md                        # Project documentation (this file)
├── PROJECT_REPORT.md                # Comprehensive 18-section academic project report
├── VIVA_QUESTIONS.md                # 30 viva questions with clear beginner-friendly answers
└── .gitignore                       # Git exclusion rules
```

---

## 📊 Dataset Details & Features

The dataset comprises **5,000 observations** across **15 columns** (14 features + 1 target variable).

### Feature Dictionary:
| Column Name | Type | Description / Range |
| :--- | :--- | :--- |
| `City` | Categorical | 10 Indian cities (e.g., Mumbai, Bangalore, Delhi, Pune, etc.) |
| `Locality` | Categorical | Specific neighborhood within the city (80 unique localities) |
| `Property_Type` | Categorical | Apartment, Independent House, Villa, Builder Floor |
| `BHK` | Discrete Numeric | Number of bedrooms, hall, kitchen (1 to 5) |
| `Bathrooms` | Discrete Numeric | Number of bathrooms (1 to 6) |
| `Super_Built_Up_Area_sqft`| Continuous Numeric | Total built-up area in square feet (400 to 4,000 sq ft) |
| `Carpet_Area_sqft` | Continuous Numeric | Net usable internal floor area (266 to 3,168 sq ft) |
| `Property_Age_years` | Continuous Numeric | Age of the construction in years (0 to 30) |
| `Furnishing_Status` | Categorical | Furnished, Semi-Furnished, Unfurnished |
| `Floor_No` | Discrete Numeric | Floor level of the property (0 = Ground floor to 29) |
| `Total_Floors` | Discrete Numeric | Total floors in the building complex (1 to 29) |
| `Parking` | Discrete Numeric | Dedicated parking spaces (0 to 3) |
| `Lift` | Binary Numeric | 1 = Lift available, 0 = Lift not available |
| `Gated_Community` | Binary Numeric | 1 = 24/7 security & gated boundary, 0 = Open standalone |
| **`Price` (Target)** | Continuous Numeric | Estimated property price in Indian Rupees (₹8,00,000 to ₹15,65,00,000) |

> ⚠️ **Important Disclosure on Dataset:**  
> This dataset is **SYNTHETIC** and algorithmically generated for educational, laboratory, and college submission purposes. It reflects standard market dynamics (e.g., Mumbai having higher base rates per sq.ft, villas commanding premium prices, floor premiums, and furnishing multipliers), but should **not** be used for genuine financial investments or real property appraisals.

---

## ⚙️ Machine Learning Pipeline

1. **Missing Value Imputation:**
   - Numerical columns: Imputed with `SimpleImputer(strategy='median')`
   - Categorical columns: Imputed with `SimpleImputer(strategy='most_frequent')`
2. **Feature Transformation & Scaling:**
   - Numerical columns: Scaled using `StandardScaler()` ($\mu = 0, \sigma = 1$).
   - Categorical columns: Encoded using `OneHotEncoder(handle_unknown='ignore', sparse_output=False)`.
3. **ColumnTransformer:**
   - Assembles both branches cleanly into an unfitted transformer.
4. **Model Integration:**
   - Combined into a complete `sklearn.pipeline.Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])`.
5. **No Data Leakage Guarantee:**
   - The preprocessor is fitted **only on the 80% training split** (`X_train`), never on `X_test`.

---

## 📈 Model Evaluation & Comparison

Both models were trained on 4,000 samples and evaluated on an independent 1,000-sample test set (80/20 train-test split, `random_state=42`):

| Evaluation Metric | Linear Regression | Random Forest Regressor | Winner |
| :--- | :--- | :--- | :--- |
| **Mean Absolute Error (MAE)** | ₹32,78,219.31 | **₹24,41,376.00** | 🏆 Random Forest (lower error by ₹8.36L) |
| **Mean Squared Error (MSE)** | $2.755 \times 10^{13}$ | **$1.884 \times 10^{13}$** | 🏆 Random Forest |
| **Root Mean Squared Error (RMSE)**| ₹52,48,999.16 | **₹43,41,260.75** | 🏆 Random Forest (lower error by ₹9.07L) |
| **Test $R^2$ Score** | 0.8179 (81.79%) | **0.8754 (87.54%)** | 🏆 Random Forest (+5.75 points higher) |
| **Train $R^2$ Score** | 0.8347 | 0.9815 | Linear Regression has smaller generalization gap |

### Why Random Forest Regressor Was Selected:
1. **Substantially Higher Explanatory Power ($R^2 = 0.8754$):** Captures non-linear feature interactions (such as the combined impact of city tier, locality premium, and luxury amenities).
2. **25.5% Lower MAE:** Reduces average prediction error by over ₹8.3 Lakhs compared to Linear Regression.
3. **Robustness to Extreme Values:** Decision trees are immune to skewness and non-linear scale steps in urban real estate.

---

## 💻 Installation & Setup

### Prerequisites
- Python 3.10+ (Tested on Python 3.13)
- pip package manager

### 1. Clone or Open Workspace
```bash
cd "c:\MY FILES\CODING\ML Project"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Step-by-Step Execution Guide

You can run each stage of the project individually via terminal commands:

### Step 1: Generate / Refresh the Dataset
```bash
python src/generate_dataset.py
```
*Output: Generates `data/house_prices.csv` with 5,000 verified rows.*

### Step 2: Verify Preprocessing Pipeline
```bash
python src/data_preprocessing.py
```
*Output: Prints exploratory statistics, column types, and pipeline structure.*

### Step 3: Generate Exploratory Data Analysis (EDA) Charts
```bash
python src/eda.py
```
*Output: Saves 8 high-resolution PNG visualizations to `outputs/charts/`.*

### Step 4: Train and Evaluate Models
```bash
python src/train_model.py
```
*Output: Trains Linear Regression & Random Forest, prints comparison table, saves `models/house_price_model.pkl`, `models/evaluation_metrics.json`, and `outputs/charts/model_comparison.png`.*

### Step 5: Test Model Inference (CLI)
```bash
python src/predict.py
```
*Output: Runs a test prediction on a sample property and outputs price in INR, Lakhs, and Crores.*

### Step 6: Run Comprehensive Automated Test Suite
```bash
python tests/test_system.py
```
*Output: Runs 8 automated test cases verifying file existence, pipeline integrity, edge cases, and currency formatting.*

### Step 7: Launch the Streamlit Web Application
```bash
streamlit run app.py
```
*Access the interactive web app at: `http://localhost:8501`*

---

## 🖥️ Streamlit Web Interface Overview (ESTATIQ Platform)

The redesigned Streamlit application (`app.py`) follows modern luxury PropTech SaaS aesthetics (Deep Navy `#101827`, Slate `#1E293B`, and Warm Gold `#D6AD60` accents):

1. **🏛️ Navigation & Brand Identity:**
   - Brand logo: **ESTATIQ** with gold monogram badge and live platform telemetry.
   - Smooth navigation between Home, Predict Price, Market Analytics, and About.
2. **✨ Hero Section:**
   - Headline: *"Find the True Market Value of Any Residential Property"*.
   - Premium architectural backdrop, metric pills, and prominent *"Predict Your Property Value"* action button.
3. **💎 Property Prediction Section (Valuation Studio):**
   - Inputs organized into 4 logical groups: Location & Archetype, Space & Layout, Building & Elevation, and Amenities.
   - Live spec sheet previewing parameters before submission.
   - Premium gold prediction trigger button.
4. **💰 Prediction Result:**
   - Displays estimated price in Indian Rupees (`₹1,84,66,000`), Lakhs (`184.66 Lakhs`), and Crores (`1.85 Crores`) with per-sq.ft. breakdown.
   - Includes real estate valuation disclaimer.
5. **📊 Market Analytics Dashboard:**
   - Interactive dark-theme Plotly visualizations: City-wise price ranking, BHK curves, Area vs. Price scatter plot, Property type distribution, and side-by-side model error benchmarks.
6. **ℹ️ About ESTATIQ:**
   - Problem statement, supervised ML algorithms (Linear Regression vs. Random Forest), technology stack matrix, and zero-data-leakage pipeline flow.
7. **📑 Footer:**
   - ESTATIQ branding, platform credits, and academic submission copyright.

---

## 🧪 Automated Test Suite

A comprehensive test suite is located at `tests/test_system.py`:

```
============================================================
RUNNING INDIAN HOUSE PRICE PREDICTION TEST SUITE
============================================================
✅ Test 1 Passed: All required project files exist.
✅ Test 2 Passed: Dataset integrity verified.
✅ Test 3 Passed: Model loaded and pipeline verified.
   ✓ Budget 1 BHK Apartment in Kolkata: ₹3,197,000
   ✓ Mid-tier 2 BHK Apartment in Bangalore: ₹10,502,000
   ✓ Luxury 4 BHK Villa in South Mumbai: ₹86,270,000
✅ Test 4 Passed: Multiple property configurations tested successfully.
✅ Test 5 Passed: Unseen categories handled gracefully (Prediction: ₹10,132,000).
✅ Test 6 Passed: Missing values imputed successfully (Prediction: ₹9,939,000).
✅ Test 7 Passed: Indian currency formatting verified.
✅ Test 8 Passed: Evaluation metrics are consistent and valid.
============================================================
🎉 ALL 8 TESTS PASSED SUCCESSFULLY!
============================================================
```

---

## ⚠️ Limitations & Future Scope

### Limitations
1. **Synthetic Nature:** While parameters follow real-world distribution curves, predictions cannot replace certified physical land appraisals.
2. **Static Inflation:** The model does not currently factor in macro-economic interest rate shifts or inflation trends over time.
3. **Absence of Spatial Geo-coordinates:** Predictions rely on discrete locality names rather than continuous GPS latitude/longitude.

### Future Scope
1. **Integration with Live APIs:** Connect to verified real estate platforms (e.g., 99acres, MagicBricks) for continuous learning.
2. **Advanced Ensembles:** Implement Gradient Boosting frameworks (XGBoost, LightGBM, CatBoost).
3. **Interactive Maps:** Embed Folium/Mapbox interactive heatmaps displaying price clusters by neighborhood.
4. **Rest API:** Package the pipeline into a FastAPI microservice for integration into mobile applications.

---

## 📄 License & Attribution

This project is developed for educational and academic submission purposes. You are free to modify, expand, and distribute this codebase for educational and research use.

#   E s t a t i q - H o u s e - P r i c e - P r e d i c t i o n  
 