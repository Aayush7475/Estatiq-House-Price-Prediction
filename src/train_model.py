"""
MODEL TRAINING SCRIPT FOR INDIAN HOUSE PRICE PREDICTION
========================================================

This script trains and evaluates machine learning models to predict house prices
in Indian cities. It uses a synthetic dataset generated for educational purposes.

Models Trained:
    1. Linear Regression   - A simple baseline model that fits a straight-line
                             relationship between features and the target price.
    2. Random Forest       - An ensemble model that builds multiple decision trees
                             and averages their predictions for better accuracy.

Workflow:
    1. Load and preprocess the dataset (via data_preprocessing.py)
    2. Split into training and testing sets
    3. Train both models using scikit-learn Pipelines
    4. Evaluate each model with MAE, MSE, RMSE, and R² metrics
    5. Select the best model based on test R² score
    6. Save the best model pipeline and evaluation metrics to disk
    7. Generate a comparison bar chart for visual analysis

Usage:
    Run from the project root directory:
        python src/train_model.py

Output Files:
    - models/house_price_model.pkl       : Saved best model pipeline (joblib)
    - models/evaluation_metrics.json     : Metrics for both models (JSON)
    - outputs/charts/model_comparison.png: Side-by-side bar chart comparing models
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

import sys
import os
import json
import warnings

# ---------------------------------------------------------------------------
# PATH SETUP: Ensure we can import sibling modules from the src/ directory.
# When this script is run as `python src/train_model.py` from the project root,
# Python's default sys.path does not include the `src/` folder. We fix that here.
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend so plots save without a GUI
import matplotlib.pyplot as plt
import joblib

# scikit-learn model classes
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

# scikit-learn evaluation metrics
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Import our custom preprocessing functions from data_preprocessing.py
from data_preprocessing import load_data, preprocess_data, split_data, build_pipeline

# Suppress non-critical warnings to keep the console output clean
warnings.filterwarnings('ignore')


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def evaluate_model(pipeline, X_train, y_train, X_test, y_test):
    """
    Evaluate a trained pipeline on both training and test data.

    This function computes four key regression metrics on the test set and also
    reports the R² on the training set (to help detect overfitting).

    Parameters:
        pipeline  : A fitted scikit-learn Pipeline object.
        X_train   : Training feature DataFrame.
        y_train   : Training target Series.
        X_test    : Test feature DataFrame.
        y_test    : Test target Series.

    Returns:
        dict: Dictionary containing MAE, MSE, RMSE, R² (test), and train_r2.
    """
    # --- Predictions ---
    y_train_pred = pipeline.predict(X_train)
    y_test_pred = pipeline.predict(X_test)

    # --- Test Metrics ---
    # MAE (Mean Absolute Error): Average of absolute differences.
    #   Tells you "on average, predictions are off by ₹X".
    mae = mean_absolute_error(y_test, y_test_pred)

    # MSE (Mean Squared Error): Average of squared differences.
    #   Penalises large errors more heavily than MAE.
    mse = mean_squared_error(y_test, y_test_pred)

    # RMSE (Root Mean Squared Error): Square root of MSE.
    #   Same units as the target (₹), easier to interpret than MSE.
    rmse = np.sqrt(mse)

    # R² (Coefficient of Determination): Proportion of variance explained.
    #   1.0 = perfect prediction, 0.0 = predicts the mean, <0 = worse than mean.
    r2 = r2_score(y_test, y_test_pred)

    # --- Training R² (for overfitting check) ---
    # If train_r2 is much higher than test r2, the model may be overfitting.
    train_r2 = r2_score(y_train, y_train_pred)

    return {
        'mae': round(float(mae), 2),
        'mse': round(float(mse), 2),
        'rmse': round(float(rmse), 2),
        'r2': round(float(r2), 4),
        'train_r2': round(float(train_r2), 4),
    }


def print_metrics_table(metrics_dict):
    """
    Print a neatly formatted comparison table of model metrics.

    Parameters:
        metrics_dict (dict): Keys are model names, values are metric dicts.
    """
    # Table header
    print("\n" + "=" * 82)
    print(f"{'Metric':<22} {'Linear Regression':>25} {'Random Forest':>25}")
    print("=" * 82)

    # Retrieve metrics for each model
    lr = metrics_dict['linear_regression']
    rf = metrics_dict['random_forest']

    # Each row: metric name, LR value, RF value
    rows = [
        ('MAE (₹)',       f"₹{lr['mae']:>15,.2f}", f"₹{rf['mae']:>15,.2f}"),
        ('MSE (₹²)',      f"{lr['mse']:>16,.2f}",   f"{rf['mse']:>16,.2f}"),
        ('RMSE (₹)',      f"₹{lr['rmse']:>15,.2f}", f"₹{rf['rmse']:>15,.2f}"),
        ('R² (Test)',     f"{lr['r2']:>16.4f}",      f"{rf['r2']:>16.4f}"),
        ('R² (Train)',    f"{lr['train_r2']:>16.4f}", f"{rf['train_r2']:>16.4f}"),
    ]

    for name, lr_val, rf_val in rows:
        print(f"  {name:<20} {lr_val:>25} {rf_val:>25}")

    print("=" * 82)


def generate_comparison_chart(metrics_dict, save_path):
    """
    Generate a grouped bar chart comparing MAE, RMSE, and R² for both models.

    The chart uses two y-axes:
      - Left axis for MAE and RMSE (currency values, ₹)
      - Right axis for R² (dimensionless, 0–1 scale)

    Parameters:
        metrics_dict (dict): Keys are model names, values are metric dicts.
        save_path (str)    : File path to save the chart image.
    """
    lr = metrics_dict['linear_regression']
    rf = metrics_dict['random_forest']

    # --- Data for the chart ---
    metric_labels = ['MAE (₹)', 'RMSE (₹)', 'R² Score']
    lr_values = [lr['mae'], lr['rmse'], lr['r2']]
    rf_values = [rf['mae'], rf['rmse'], rf['r2']]

    # --- Create figure with two y-axes ---
    fig, ax1 = plt.subplots(figsize=(12, 7))

    x = np.arange(len(metric_labels))  # label positions
    bar_width = 0.30

    # Colours inspired by a professional palette
    color_lr = '#4A90D9'   # Blue for Linear Regression
    color_rf = '#2ECC71'   # Green for Random Forest

    # Bars for MAE and RMSE (left y-axis, ₹ values)
    bars1_lr = ax1.bar(x[:2] - bar_width / 2, lr_values[:2], bar_width,
                       label='Linear Regression', color=color_lr, edgecolor='white',
                       linewidth=0.8)
    bars1_rf = ax1.bar(x[:2] + bar_width / 2, rf_values[:2], bar_width,
                       label='Random Forest', color=color_rf, edgecolor='white',
                       linewidth=0.8)

    ax1.set_ylabel('Error Amount (₹)', fontsize=12, fontweight='bold')
    ax1.tick_params(axis='y', labelsize=10)

    # Add value labels on top of MAE/RMSE bars
    for bar in list(bars1_lr) + list(bars1_rf):
        height = bar.get_height()
        ax1.annotate(f'₹{height:,.0f}',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 5), textcoords='offset points',
                     ha='center', va='bottom', fontsize=8, fontweight='bold')

    # --- Second y-axis for R² ---
    ax2 = ax1.twinx()

    bars2_lr = ax2.bar(x[2] - bar_width / 2, lr_values[2], bar_width,
                       color=color_lr, edgecolor='white', linewidth=0.8)
    bars2_rf = ax2.bar(x[2] + bar_width / 2, rf_values[2], bar_width,
                       color=color_rf, edgecolor='white', linewidth=0.8)

    ax2.set_ylabel('R² Score', fontsize=12, fontweight='bold')
    ax2.set_ylim(0, 1.15)  # Give headroom for labels
    ax2.tick_params(axis='y', labelsize=10)

    # Add value labels on R² bars
    for bar in list(bars2_lr) + list(bars2_rf):
        height = bar.get_height()
        ax2.annotate(f'{height:.4f}',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 5), textcoords='offset points',
                     ha='center', va='bottom', fontsize=9, fontweight='bold')

    # --- Axis labels and formatting ---
    ax1.set_xticks(x)
    ax1.set_xticklabels(metric_labels, fontsize=12, fontweight='bold')

    plt.title('Model Comparison: Linear Regression vs Random Forest\n'
              'Indian House Price Prediction (Synthetic Data)',
              fontsize=14, fontweight='bold', pad=15)

    # Combined legend
    ax1.legend(loc='upper left', fontsize=11, framealpha=0.9)

    # Light grid for readability
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_axisbelow(True)

    fig.tight_layout()

    # --- Save ---
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)

    print(f"📊 Comparison chart saved to: {save_path}")


# ==============================================================================
# MAIN TRAINING WORKFLOW
# ==============================================================================

def main():
    """
    Main function that orchestrates the entire training pipeline:
      1. Load data → 2. Preprocess → 3. Split → 4. Train → 5. Evaluate →
      6. Select best → 7. Save model & metrics → 8. Generate chart
    """

    # --- Resolve project root (one level up from src/) ---
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(project_root, 'data', 'house_prices.csv')

    print("=" * 70)
    print("     INDIAN HOUSE PRICE PREDICTION — MODEL TRAINING")
    print("=" * 70)
    print()

    # =========================================================================
    # STEP 1: Load the dataset
    # =========================================================================
    print("📂 Step 1: Loading dataset...")
    df = load_data(data_path)
    print(f"   ✅ Dataset loaded — {df.shape[0]} rows, {df.shape[1]} columns")
    print()

    # =========================================================================
    # STEP 2: Preprocess the dataset
    # =========================================================================
    print("🔧 Step 2: Preprocessing data...")
    X, y, preprocessor = preprocess_data(df)
    print(f"   ✅ Features (X): {X.shape}")
    print(f"   ✅ Target  (y): {y.shape}")
    print()

    # =========================================================================
    # STEP 3: Split into training and testing sets
    # =========================================================================
    print("✂️  Step 3: Splitting data into train/test sets (80/20)...")
    X_train, X_test, y_train, y_test = split_data(X, y)
    print(f"   📊 Training set size : {X_train.shape[0]} samples")
    print(f"   📊 Testing  set size : {X_test.shape[0]} samples")
    print()

    # =========================================================================
    # STEP 4: Define models
    # =========================================================================
    # We store each model with a friendly name and its sklearn estimator object.
    models = {
        'linear_regression': LinearRegression(),
        'random_forest': RandomForestRegressor(
            n_estimators=100,      # Number of trees in the forest
            random_state=42,       # Fixed seed for reproducibility
        ),
    }

    # =========================================================================
    # STEP 5: Train and evaluate each model
    # =========================================================================
    print("🤖 Step 4–5: Training and evaluating models...")
    print("-" * 70)

    all_metrics = {}       # Will hold evaluation metrics for every model
    trained_pipelines = {} # Will hold fitted Pipeline objects

    for model_name, model in models.items():
        print(f"\n   ▶ Training: {model_name.replace('_', ' ').title()} ...")

        # Build a full Pipeline: preprocessor → model
        # The preprocessor handles encoding, scaling, etc.
        # The model does the actual learning.
        pipeline = build_pipeline(preprocessor, model)

        # Fit the pipeline on training data ONLY
        pipeline.fit(X_train, y_train)
        print(f"     ✅ Training complete.")

        # Evaluate on both train and test sets
        metrics = evaluate_model(pipeline, X_train, y_train, X_test, y_test)
        all_metrics[model_name] = metrics
        trained_pipelines[model_name] = pipeline

        # Quick summary for this model
        print(f"     📈 Test  R² = {metrics['r2']:.4f}")
        print(f"     📈 Train R² = {metrics['train_r2']:.4f}")
        print(f"     📈 MAE     = ₹{metrics['mae']:,.2f}")
        print(f"     📈 RMSE    = ₹{metrics['rmse']:,.2f}")

    # =========================================================================
    # STEP 6: Print detailed comparison table
    # =========================================================================
    print_metrics_table(all_metrics)

    # =========================================================================
    # STEP 7: Select the best model based on test R²
    # =========================================================================
    # R² is chosen because it is scale-independent and tells us what proportion
    # of the variance in house prices our model can explain.
    best_model_name = max(all_metrics, key=lambda name: all_metrics[name]['r2'])
    best_r2 = all_metrics[best_model_name]['r2']

    print(f"\n🏆 Best Model: {best_model_name.replace('_', ' ').title()}")
    print(f"   Reason: Highest test R² score = {best_r2:.4f}")

    # Check for potential overfitting in the best model
    train_r2_best = all_metrics[best_model_name]['train_r2']
    r2_gap = train_r2_best - best_r2
    if r2_gap > 0.10:
        print(f"   ⚠️  Note: Train R² ({train_r2_best:.4f}) is notably higher "
              f"than Test R² ({best_r2:.4f}). Gap = {r2_gap:.4f}.")
        print(f"       This may indicate some overfitting. Consider tuning "
              f"hyperparameters or adding regularisation.")

    # =========================================================================
    # STEP 8: Save the best model pipeline to disk
    # =========================================================================
    model_dir = os.path.join(project_root, 'models')
    os.makedirs(model_dir, exist_ok=True)

    model_save_path = os.path.join(model_dir, 'house_price_model.pkl')
    joblib.dump(trained_pipelines[best_model_name], model_save_path)
    print(f"\n💾 Best model pipeline saved to: {model_save_path}")

    # =========================================================================
    # STEP 9: Save evaluation metrics to JSON
    # =========================================================================
    # Build the JSON structure with metrics for both models + best model info
    metrics_output = {
        'linear_regression': all_metrics['linear_regression'],
        'random_forest': all_metrics['random_forest'],
        'best_model': best_model_name,
        'best_model_r2': best_r2,
    }

    metrics_save_path = os.path.join(model_dir, 'evaluation_metrics.json')
    with open(metrics_save_path, 'w', encoding='utf-8') as f:
        json.dump(metrics_output, f, indent=4, ensure_ascii=False)

    print(f"📄 Evaluation metrics saved to: {metrics_save_path}")

    # =========================================================================
    # STEP 10: Generate comparison chart
    # =========================================================================
    chart_dir = os.path.join(project_root, 'outputs', 'charts')
    chart_path = os.path.join(chart_dir, 'model_comparison.png')
    generate_comparison_chart(all_metrics, chart_path)

    # =========================================================================
    # FINAL SUMMARY
    # =========================================================================
    print("\n" + "=" * 70)
    print("     TRAINING COMPLETE — SUMMARY")
    print("=" * 70)
    print(f"  📊 Training samples  : {X_train.shape[0]}")
    print(f"  📊 Testing  samples  : {X_test.shape[0]}")
    print(f"  🏆 Best model        : {best_model_name.replace('_', ' ').title()}")
    print(f"  📈 Best test R²      : {best_r2:.4f}")
    print(f"  💾 Model file        : {model_save_path}")
    print(f"  📄 Metrics file      : {metrics_save_path}")
    print(f"  📊 Chart file        : {chart_path}")
    print("=" * 70)
    print()


# ==============================================================================
# ENTRY POINT
# ==============================================================================
# The `if __name__ == '__main__':` guard ensures that `main()` runs only when
# this script is executed directly (e.g., `python train_model.py`), and NOT
# when it is imported as a module by another script.
# ==============================================================================

if __name__ == '__main__':
    main()
