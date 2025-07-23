import pandas as pd
import numpy as np
from geopy.distance import geodesic
from sklearn.neighbors import KNeighborsClassifier
import joblib

# Load data
orders = pd.read_csv("../data/orders.csv")
warehouses = pd.read_csv("../data/warehouses.csv")

# Sort by urgency
urgency_map = {"High": 0, "Medium": 1, "Low": 2}
orders["urgency_rank"] = orders["urgency"].map(urgency_map)
orders = orders.sort_values(by="urgency_rank")

assignments = []
X_train, y_train = [], []

for _, order in orders.iterrows():
    eligible = warehouses[warehouses["stock"] >= order["quantity"]]
    if eligible.empty:
        assignments.append((order["id"], "Unassigned"))
        continue

    eligible["distance"] = eligible.apply(
        lambda wh: geodesic(
            (order["latitude"], order["longitude"]),
            (wh["latitude"], wh["longitude"])
        ).km,
        axis=1
    )

    nearest = eligible.loc[eligible["distance"].idxmin()]
    warehouses.loc[warehouses["id"] == nearest["id"], "stock"] -= order["quantity"]
    assignments.append((order["id"], nearest["name"]))

    X_train.append([order["latitude"], order["longitude"], order["quantity"], urgency_map[order["urgency"]]])
    y_train.append(nearest["name"])

assignments_df = pd.DataFrame(assignments, columns=["order_id", "assigned_warehouse"])
assignments_df.to_csv("../data/assignments.csv", index=False)
print(assignments_df)

# Train Smart Suggestion Engine
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)
joblib.dump(knn, "../models/warehouse_suggestion_model.pkl")
print("Smart Warehouse Suggestion Engine trained and saved.")
