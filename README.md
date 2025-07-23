# Smart Order Fulfillment System (Extended Version)

## Overview
This extended project adds urgency-based dispatching and a machine learning model that learns to suggest the best warehouse based on historical data.

## Features
- Sorts orders by urgency (High > Medium > Low)
- Assigns orders to nearest warehouse with stock
- Trains a KNN model to learn dispatch patterns
- Outputs both CSV results and a saved ML model

## How to Run
1. Create and activate a virtual environment
2. Install requirements:
   ```
   pip install -r requirements.txt
   ```
3. Run the dispatcher:
   ```
   cd src
   python dispatch_simulation.py
   ```
4. Check:
   - `data/assignments.csv` for results
   - `models/warehouse_suggestion_model.pkl` for ML model

## Requirements
- Python 3.7+
- pandas
- geopy
- scikit-learn
- joblib
