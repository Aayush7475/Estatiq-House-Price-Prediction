# ACADEMIC PROJECT REPORT

## PROJECT TITLE:
# INDIAN HOUSE PRICE PREDICTION SYSTEM
### A Machine Learning-Based Supervised Regression System for Urban Residential Property Valuation in India

---

**Academic Degree:** Bachelor of Technology (B.Tech) in Computer Science & Engineering  
**Subject:** Machine Learning Laboratory / Capstone Project  
**Submission Deadline:** 3-Day Rapid Prototype Submission  
**Implementation Platform:** Python 3.13, Scikit-learn, Streamlit, Pandas, NumPy, Matplotlib, Plotly  

---

## TABLE OF CONTENTS
1. [Abstract](#1-abstract)
2. [Introduction](#2-introduction)
3. [Problem Statement](#3-problem-statement)
4. [Objectives](#4-objectives)
5. [Existing System](#5-existing-system)
6. [Proposed System](#6-proposed-system)
7. [Dataset Description](#7-dataset-description)
8. [Data Preprocessing](#8-data-preprocessing)
9. [Exploratory Data Analysis (EDA)](#9-exploratory-data-analysis-eda)
10. [Algorithms Used](#10-algorithms-used)
11. [System Architecture](#11-system-architecture)
12. [Model Training](#12-model-training)
13. [Model Evaluation](#13-model-evaluation)
14. [Results and Discussion](#14-results-and-discussion)
15. [Limitations](#15-limitations)
16. [Future Scope](#16-future-scope)
17. [Conclusion](#17-conclusion)
18. [References](#18-references)

---

## 1. ABSTRACT

Valuation of residential real estate in India presents complex predictive challenges due to significant price discrepancies across regional geographies, varying amenities, construction age, and neighborhood premiums. This project presents an end-to-end Machine Learning solution—the **Indian House Price Prediction System**—which predicts the estimated market valuation of residential properties across ten major Indian metropolitan centers (Mumbai, Delhi, Bangalore, Hyderabad, Chennai, Pune, Kolkata, Ahmedabad, Jaipur, and Lucknow). 

The system leverages a supervised machine learning regression pipeline built with Scikit-learn, integrating automated missing-value imputation, standard scaling, and one-hot categorical encoding via a consolidated `ColumnTransformer`. Two primary regression architectures were evaluated: a parametric baseline (**Linear Regression**) and a non-parametric ensemble model (**Random Forest Regressor** with 100 estimators). Models were trained on 80% (4,000 samples) of a 5,000-record dataset and validated on an unseen 20% holdout test set (1,000 samples). 

The Random Forest Regressor emerged as the optimal architecture, attaining a test Coefficient of Determination ($R^2$) of **0.8754**, Mean Absolute Error (MAE) of **₹24,41,376.00**, and Root Mean Squared Error (RMSE) of **₹43,41,260.75**, outperforming Linear Regression ($R^2 = 0.8179$, MAE = ₹32,78,219.31) by over 25.5% in error reduction. The trained pipeline was serialized using Joblib and deployed through a professional 5-page interactive web application constructed with Streamlit. The interface enables end-users to input custom property specifications, receive real-time property valuations formatted in Indian numbering nomenclature (Rupees, Lakhs, Crores), and explore dynamic market analytics.

---

## 2. INTRODUCTION

Real estate represents one of the most critical sectors of the Indian economy, accounting for substantial capital formation and household wealth. However, residential property pricing in Indian urban markets is characterized by information asymmetry, high non-linearity, and subjective pricing decisions by property brokers and developers.

With rapid advancements in Data Science and Machine Learning, historical transaction features can be harnessed to construct predictive statistical estimators capable of assessing property values objectively. A well-designed predictive model eliminates emotional bias, standardizes pricing evaluations, and aids prospective buyers, financial lending institutions, and developers in estimating real property values based on concrete physical and location attributes.

This project delivers a complete, modular, and reproducible supervised machine learning regression system. Developed within a 3-day engineering scope, it follows industry best practices:
- Modular Python package structure.
- Encapsulated preprocessing avoiding data leakage.
- Rigorous statistical error benchmarking (MAE, MSE, RMSE, $R^2$).
- Intuitive user interface with interactive data visualization.
- Automated verification via integration test suites.

---

## 3. PROBLEM STATEMENT

In conventional Indian real estate markets:
1. **Lack of Transparency:** Real estate pricing is largely dictated by local intermediaries who often quote arbitrary or inflated numbers.
2. **Multi-Factor Interaction:** Property prices are not simply a linear function of square footage; they depend on non-linear combinations of city tier, locality desirability, property type (e.g., apartment vs. villa), floor height, building age depreciation, parking availability, and gated security.
3. **Absence of Accessible Valuation Tools:** Individual home buyers and students lack accessible, easy-to-use software tools capable of providing instant, data-backed property price estimates formatted in standard Indian monetary conventions (Lakhs and Crores).

Therefore, there is a clear academic and practical need to develop an automated predictive system that ingests key residential attributes and outputs reliable price estimates.

---

## 4. OBJECTIVES

The specific technical objectives of this project are:
1. **Dataset Design:** Acquire or construct a comprehensive, structured dataset comprising residential features across 10 major Indian metropolitan cities.
2. **Data Preprocessing & Leakage Prevention:** Implement a Scikit-learn `Pipeline` utilizing `ColumnTransformer` to handle imputation, standard scaling, and one-hot encoding without data leakage between training and testing splits.
3. **Exploratory Data Analysis (EDA):** Perform in-depth statistical data analysis and generate high-resolution visual artifacts detailing price distributions, feature correlations, and categorical trends.
4. **Model Development & Benchmarking:** Train, tune, and evaluate at least two distinct regression models (**Linear Regression** and **Random Forest Regressor**) using standard regression metrics: MAE, MSE, RMSE, and $R^2$.
5. **Model Persistence:** Serialize the superior pipeline using `joblib` into a deployable artifact (`models/house_price_model.pkl`).
6. **Frontend Web Application:** Develop an interactive, responsive Streamlit dashboard featuring multi-page navigation, dynamic locality selectors, instant prediction calculators, and Plotly interactive data visualizations.
7. **System Verification:** Write and execute an automated test suite verifying file integrity, model stability, edge-case tolerance (unseen categories, missing values), and currency conversions.

---

## 5. EXISTING SYSTEM

Historically, property valuation in the Indian context has relied on:
- **Brokerage Assessment:** Informal estimations provided by local property brokers who rely on personal memory and anecdotal transaction history.
- **Guidance Value / Circle Rates:** Government-published circle rates that establish baseline property taxes, which often lag actual open-market transaction prices by 30% to 100%.
- **Basic Spreadsheet Calculations:** Rudimentary linear rules of thumb (e.g., multiplying average square-foot rates by built-up area), completely ignoring floor height premiums, depreciation curves, or security amenities.

### Shortcomings of the Existing System:
- Highly prone to human bias and speculation.
- Inability to capture complex multivariate non-linear patterns.
- High barrier of entry and lack of self-service accessibility for common citizens.

---

## 6. PROPOSED SYSTEM

The **Indian House Price Prediction System** replaces subjective estimates with an empirical machine learning regression pipeline.

```
+-----------------------------------------------------------------------------------+
|                                 PROPOSED SYSTEM                                   |
|                                                                                   |
|  [User Input Form]                                                                |
|         │                                                                         |
|         ▼                                                                         |
|  [Raw Feature Dictionary]                                                         |
|         │                                                                         |
|         ▼                                                                         |
|  [Scikit-learn Pipeline]                                                          |
|         ├── Categorical Pipeline (SimpleImputer → OneHotEncoder)                  |
|         └── Numerical Pipeline   (SimpleImputer → StandardScaler)                 |
|         │                                                                         |
|         ▼                                                                         |
|  [Trained Random Forest Regressor]                                                |
|         │                                                                         |
|         ▼                                                                         |
|  [Predicted Price in ₹ (INR)] ──→ [Indian Currency Formatter]                     |
|                                         ├── Price in ₹ Numbers                    |
|                                         ├── Price in Lakhs (₹ L)                  |
|                                         └── Price in Crores (₹ Cr)                |
+-----------------------------------------------------------------------------------+
```

### Key Advantages:
1. **Data-Driven & Objective:** Evaluates properties purely based on statistical feature weights and decision tree splits.
2. **Instant Feedback:** Generates predictions in less than 50 milliseconds via compiled pipeline inference.
3. **Comprehensive Coverage:** Supports 10 cities and over 80 localities.
4. **End-to-End Pipeline Safety:** Preprocessing parameters (means, standard deviations, categorical vocabularies) are frozen within the serialized artifact, preventing runtime data drift.

---

## 7. DATASET DESCRIPTION

In accordance with project guidelines, the workspace was first inspected for existing raw real estate CSV files. To ensure immediate reproducibility, prevent reliance on authenticated third-party APIs, and strictly avoid fabricating real-world records as actual market listings, an algorithmic **synthetic dataset** generator was constructed (`src/generate_dataset.py`).

The generator models realistic Indian urban real estate relationships:
- City base square-foot price tiers (Mumbai highest at ₹18,000/sq.ft base; Lucknow at ₹4,000/sq.ft base).
- Locality price multipliers reflecting prime vs. suburban corridors.
- Property type multipliers (Villas = 1.8x, Independent Houses = 1.3x, Apartments = 1.0x).
- Depreciation penalty applied to aging properties (-0.8% per year).
- Floor-rise premiums for high-rise buildings (+5% upper floor advantage).
- Controlled random noise ($\pm 15\%$) reflecting unobserved variance.

### Dataset Specifications:
- **Total Records:** 5,000
- **Total Features:** 14 independent features + 1 target variable (`Price`)
- **Missing Values:** 0
- **Duplicate Records:** 0

### Complete Feature List:
| Feature Name | Type | Data Nature | Domain / Range |
| :--- | :--- | :--- | :--- |
| `City` | Categorical | Text | 10 Cities: Mumbai, Delhi, Bangalore, Hyderabad, Chennai, Pune, Kolkata, Ahmedabad, Jaipur, Lucknow |
| `Locality` | Categorical | Text | 80 neighborhoods (e.g., Bandra, Koramangala, Whitefield, OMR) |
| `Property_Type` | Categorical | Text | Apartment, Independent House, Villa, Builder Floor |
| `BHK` | Numerical | Discrete | 1, 2, 3, 4, 5 |
| `Bathrooms` | Numerical | Discrete | 1 to 6 |
| `Super_Built_Up_Area_sqft`| Numerical | Continuous | 400 to 3,999 sq ft |
| `Carpet_Area_sqft` | Numerical | Continuous | 266 to 3,168 sq ft (65% to 80% of built-up area) |
| `Property_Age_years` | Numerical | Continuous | 0 to 30 years |
| `Furnishing_Status` | Categorical | Text | Furnished, Semi-Furnished, Unfurnished |
| `Floor_No` | Numerical | Discrete | 0 (Ground) to 29 |
| `Total_Floors` | Numerical | Discrete | 1 to 29 |
| `Parking` | Numerical | Discrete | 0, 1, 2, 3 parking slots |
| `Lift` | Numerical | Binary | 0 = No, 1 = Yes |
| `Gated_Community` | Numerical | Binary | 0 = No, 1 = Yes |
| **`Price` (Target)** | Numerical | Continuous | ₹8,00,000 to ₹15,65,00,000 (Mean: ₹1,40,28,300) |

---

## 8. DATA PREPROCESSING

Data preprocessing was designed in accordance with rigorous machine learning standards to avoid **Data Leakage**.

### Preprocessing Architecture:
```
                         ┌─ SimpleImputer(median) ─→ StandardScaler() ────────┐
Raw Input (14 features) ─┤                                                    ├─→ Combined Features (97 dims)
                         └─ SimpleImputer(most_freq) ─→ OneHotEncoder(ignore) ┘
```

1. **Numerical Pipeline:**
   - Numerical Columns (10): `BHK`, `Bathrooms`, `Super_Built_Up_Area_sqft`, `Carpet_Area_sqft`, `Property_Age_years`, `Floor_No`, `Total_Floors`, `Parking`, `Lift`, `Gated_Community`.
   - Transformation: Missing numerical inputs are imputed using the **median** value of the training set. Values are then standardized via `StandardScaler`:
     $$z = \frac{x - \mu}{\sigma}$$
     where $\mu$ is the training feature mean and $\sigma$ is the standard deviation.

2. **Categorical Pipeline:**
   - Categorical Columns (4): `City`, `Locality`, `Property_Type`, `Furnishing_Status`.
   - Transformation: Missing text values are filled with the **most frequent** category. Features are converted into binary vectors using `OneHotEncoder(handle_unknown='ignore', sparse_output=False)`. Setting `handle_unknown='ignore'` guarantees that novel categories encountered during production inference evaluate to all zeros rather than crashing the system.

3. **Data Splitting:**
   - The dataset was split into **80% training** ($N = 4,000$) and **20% testing** ($N = 1,000$) using `sklearn.model_selection.train_test_split` with `random_state=42`.
   - Transformations were **fitted strictly on the training set** (`preprocessor.fit(X_train)`), and applied to `X_test` via `transform()` only.

---

## 9. EXPLORATORY DATA ANALYSIS (EDA)

Exploratory Data Analysis was executed via `src/eda.py` using `matplotlib` and `seaborn`. Eight dedicated visualizations were generated and saved to `outputs/charts/`:

1. **`price_distribution.png` (Price Distribution):**
   - Displays a right-skewed unimodal distribution typical of housing markets, with the mass of residential properties priced between ₹40 Lakhs and ₹1.8 Crores, and a long tail extending up to ₹15.65 Crores for high-end luxury villas in Mumbai and South Delhi.
2. **`avg_price_by_city.png` (City-wise Average Prices):**
   - Confirms that Mumbai holds the highest average property price (~₹2.5 Cr), followed by Delhi (~₹1.8 Cr) and Bangalore (~₹1.3 Cr), with Lucknow and Jaipur offering the most affordable housing baselines.
3. **`price_vs_area.png` (Area vs. Price Scatter Plot):**
   - Illustrates a strong positive linear-to-quadratic correlation between super built-up area and property price, with villas demonstrating steeper pricing slopes compared to standard apartments.
4. **`bhk_vs_price.png` (BHK vs. Price Boxplot):**
   - Boxplots show a stepwise escalation in median prices from 1 BHK (~₹35 Lakhs) up to 5 BHK (>₹4.5 Crores), with expanding interquartile ranges (IQR) in higher configurations reflecting greater amenity variance.
5. **`property_type_comparison.png` (Property Type Valuation):**
   - Highlights that Villas command the highest valuation on average, followed by Independent Houses, Builder Floors, and Apartments.
6. **`correlation_heatmap.png` (Numerical Correlation Matrix):**
   - Shows highest positive correlation with `Price` from `Super_Built_Up_Area_sqft` ($r \approx 0.72$), `Carpet_Area_sqft` ($r \approx 0.70$), `BHK` ($r \approx 0.58$), and `Bathrooms` ($r \approx 0.55$).
7. **`numerical_distributions.png` (Feature Histograms Grid):**
   - Validates feature distributions across property ages, total floors, parking availability, and room counts.
8. **`furnishing_vs_price.png` (Furnishing Impact):**
   - Fully furnished properties command an average premium of 12–15% over unfurnished units.

---

## 10. ALGORITHMS USED

Two contrasting regression algorithms were selected to test different functional paradigms:

### 10.1 Linear Regression (Parametric Baseline)
Linear Regression models the target variable $y$ as a linear combination of input features $x$:
$$\hat{y} = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \dots + \beta_p x_p + \epsilon$$

The parameter vector $\boldsymbol{\beta}$ is computed analytically using Ordinary Least Squares (OLS):
$$\boldsymbol{\beta} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}$$

- **Strengths:** Computationally rapid, highly interpretable, serves as an essential linear benchmark.
- **Weaknesses:** Cannot model complex non-linear interactions without manual polynomial expansion; sensitive to outliers.

### 10.2 Random Forest Regressor (Non-Parametric Ensemble)
Random Forest is a bagging (Bootstrap Aggregation) ensemble of unpruned Decision Trees:
$$\hat{y} = \frac{1}{B} \sum_{b=1}^{B} T_b(\mathbf{x})$$

For each tree $T_b$:
1. A bootstrap sample of size $N$ is drawn with replacement from the training data.
2. At each candidate split node, a random subset of $m \approx \sqrt{p}$ features is evaluated.
3. The split that minimizes the Mean Squared Error (variance reduction) is selected:
   $$\text{MSE}_{\text{split}} = \frac{1}{N_L} \sum_{i \in L} (y_i - \bar{y}_L)^2 + \frac{1}{N_R} \sum_{i \in R} (y_i - \bar{y}_R)^2$$

- **Configuration:** `n_estimators=100`, `random_state=42`.
- **Strengths:** Captures non-linear relationships, robust to outliers, naturally handles multi-collinearity and high-dimensional categorical features.

---

## 11. SYSTEM ARCHITECTURE

The overall end-to-end system architecture is partitioned into four clear modules:

```
[ Data Layer ]
      │  └── data/house_prices.csv (5,000 records)
      ▼
[ Engineering & Training Layer ]
      │  ├── src/data_preprocessing.py (Imputer, Scaler, Encoder, Splitter)
      │  ├── src/train_model.py        (Linear Regression vs Random Forest)
      │  └── src/eda.py                (Statistical plotting engine)
      ▼
[ Artifact & Model Persistence Layer ]
      │  ├── models/house_price_model.pkl   (Trained sklearn Pipeline)
      │  ├── models/evaluation_metrics.json (Logged validation metrics)
      │  └── outputs/charts/                (8 PNG visual artifacts)
      ▼
[ Presentation & Serving Layer ]
         ├── app.py           (Interactive 5-Page Streamlit Dashboard)
         ├── src/predict.py   (Inference pipeline & INR formatting)
         └── tests/test_system.py (Automated test suite)
```

---

## 12. MODEL TRAINING

Model training was conducted systematically in `src/train_model.py`:

1. Preprocessing and modeling steps were joined inside a single `Pipeline`:
   ```python
   pipeline = Pipeline(steps=[
       ('preprocessor', preprocessor),
       ('model', regressor)
   ])
   ```
2. The pipeline was fitted exclusively on the training set:
   ```python
   pipeline.fit(X_train, y_train)
   ```
3. Training and testing predictions were generated:
   ```python
   y_train_pred = pipeline.predict(X_train)
   y_test_pred  = pipeline.predict(X_test)
   ```
4. Both pipelines were evaluated under identical cross-validation conditions with `random_state=42`.

---

## 13. MODEL EVALUATION

To provide a rigorous academic evaluation, four standard regression metrics were computed on the independent 1,000-sample test set:

1. **Mean Absolute Error (MAE):**
   $$\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|$$
   Measures average absolute deviation in the original unit (₹ INR).

2. **Mean Squared Error (MSE):**
   $$\text{MSE} = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$$
   Measures expected squared deviation, heavily penalizing large outliers.

3. **Root Mean Squared Error (RMSE):**
   $$\text{RMSE} = \sqrt{\text{MSE}}$$
   Restores error dimensionality to Indian Rupees (₹ INR).

4. **Coefficient of Determination ($R^2$):**
   $$R^2 = 1 - \frac{\sum_{i=1}^{n} (y_i - \hat{y}_i)^2}{\sum_{i=1}^{n} (y_i - \bar{y})^2}$$
   Measures the proportion of target variance explained by the model features (where $R^2 \le 1.0$; note that $R^2$ is **not** percentage accuracy).

---

## 14. RESULTS AND DISCUSSION

### 14.1 Quantitative Performance Summary

| Metric | Linear Regression | Random Forest Regressor | Absolute Difference | Relative Improvement |
| :--- | :--- | :--- | :--- | :--- |
| **Test $R^2$ Score** | **0.8179** | **0.8754** | **+0.0575** | **+7.0% improvement in variance explained** |
| **Train $R^2$ Score**| 0.8347 | 0.9815 | +0.1468 | High expressive capacity |
| **MAE (₹)** | ₹32,78,219.31 | **₹24,41,376.00** | **-₹8,36,843.31** | **25.53% error reduction** |
| **MSE (₹²)** | $2.755 \times 10^{13}$ | **$1.884 \times 10^{13}$** | $-8.705 \times 10^{12}$| 31.60% MSE reduction |
| **RMSE (₹)** | ₹52,48,999.16 | **₹43,41,260.75** | **-₹9,07,738.41** | **17.29% RMSE reduction** |

### 14.2 Discussion
- **Model Selection:** The **Random Forest Regressor** outperformed Linear Regression across all test metrics, achieving an $R^2$ of **0.8754** compared to 0.8179. It reduced the Mean Absolute Error from ₹32.78 Lakhs down to ₹24.41 Lakhs—an average improvement of ₹8.36 Lakhs per property estimation.
- **Non-Linear Interactions:** Housing valuation exhibits high non-linearity (e.g., floor rise premium is negligible in low-tier builder floors but significant in luxury high-rises; villa land-area valuation differs fundamentally from apartment super built-up ratios). Random Forest successfully partitions feature space into hierarchical decision rules that capture these interactions.
- **Overfitting Analysis:** The training $R^2$ for Random Forest was 0.9815 versus test $R^2$ of 0.8754 (a difference of 0.1061). This mild generalization gap is standard for unconstrained decision tree ensembles and can be further minimized through hyperparameter pruning (`max_depth`, `min_samples_split`).

The final pipeline containing the Random Forest Regressor and fitted `ColumnTransformer` was saved to `models/house_price_model.pkl` (File size: ~28 MB).

---

## 15. LIMITATIONS

While the system is robust, several academic and engineering limitations should be noted:
1. **Synthetic Data Foundation:** Because authenticated live access to proprietary portals (MagicBricks/99acres) was restricted, the dataset was synthesized algorithmically. While realistic, it cannot substitute for legal certified land appraisals.
2. **Absence of Temporal Inflation Modeling:** Real estate values fluctuate with interest rates and inflation; the current model treats all observations as contemporary cross-sectional data.
3. **Discrete Locality Encoding:** Localities are treated as discrete categorical buckets. Contiguous geographical boundaries (latitude/longitude coordinates) are not currently utilized.
4. **Uncaptured Micro-Attributes:** Factors such as exact road width, view orientation (Vaastu compliance), water table depth, and developer reputation were not present in the dataset schema.

---

## 16. FUTURE SCOPE

For future iterations and capstone enhancements:
1. **Integration with Real-World Listing APIs:** Connect to open real-estate aggregators or scraping pipelines to periodically ingest live market transactions.
2. **Gradient Boosting Ensembles:** Benchmark against advanced gradient-boosted decision trees including **XGBoost**, **LightGBM**, and **CatBoost**.
3. **Geospatial Feature Engineering:** Incorporate continuous latitude, longitude, and GIS distance matrices to key hubs (metro stations, airports, tech parks).
4. **Automated MLOps Pipeline:** Implement continuous retraining with MLflow and containerize the system using Docker and Kubernetes.
5. **Computer Vision Integration:** Train a Convolutional Neural Network (CNN) on property interior and exterior photos to compute a physical condition score fed directly into the tabular regression pipeline.

---

## 17. CONCLUSION

The **Indian House Price Prediction System** successfully accomplishes all stated technical objectives. An end-to-end supervised machine learning pipeline was constructed, encompassing data generation, pre-processing, exploratory visualization, model benchmarking, and full-stack web deployment within an accelerated 3-day timeframe.

The project demonstrates:
- How Scikit-learn's `Pipeline` and `ColumnTransformer` prevent data leakage while handling mixed-type tabular data.
- The decisive superiority of ensemble learning (**Random Forest Regressor**, $R^2 = 0.8754$) over classical parametric models (**Linear Regression**, $R^2 = 0.8179$) in handling non-linear pricing dynamics.
- How Streamlit enables rapid deployment of data science artifacts into accessible, consumer-friendly web dashboards with dynamic Indian currency formatting.
- Thorough testing and validation through an 8-stage automated test suite.

The resulting software artifact represents a comprehensive, fully functional, and academically rigorous Machine Learning project ready for university evaluation and laboratory submission.

---

## 18. REFERENCES

1. Géron, A. (2019). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow: Concepts, Tools, and Techniques to Build Intelligent Systems*. O'Reilly Media.
2. Pedregosa, F., et al. (2011). *Scikit-learn: Machine Learning in Python*. Journal of Machine Learning Research, 12, 2825-2830.
3. Breiman, L. (2001). *Random Forests*. Machine Learning, 45(1), 5-32.
4. McKinney, W. (2010). *Data Structures for Statistical Computing in Python*. Proceedings of the 9th Python in Science Conference, 51-56.
5. Streamlit Documentation. *Streamlit: The fastest way to build and share data apps*. https://docs.streamlit.io.
6. Indian Urban Real Estate Market Reports (2023–2024). Knight Frank India / Anarock Property Consultants Research Publications.

