import streamlit as st
import pandas as pd
from geopy.distance import geodesic

st.title("📦 Smart Order Fulfillment Dashboard")

uploaded_orders = st.file_uploader("Upload Orders CSV", type="csv")
uploaded_warehouses = st.file_uploader("Upload Warehouses CSV", type="csv")

if uploaded_orders and uploaded_warehouses:
    orders = pd.read_csv(uploaded_orders)
    warehouses = pd.read_csv(uploaded_warehouses)

    assignments = []

    for _, order in orders.iterrows():
        order_location = (order['latitude'], order['longitude'])
        suitable_warehouse = None
        min_distance = float('inf')

        for i, warehouse in warehouses.iterrows():
            wh_location = (warehouse['latitude'], warehouse['longitude'])
            distance = geodesic(order_location, wh_location).km
            if warehouse['stock'] >= order['quantity'] and distance < min_distance:
                suitable_warehouse = warehouse
                min_distance = distance

        if suitable_warehouse is not None:
            assignments.append({
                "order_id": order['order_id'],
                "warehouse_id": suitable_warehouse['warehouse_id'],
                "distance_km": round(min_distance, 2),
                "status": "Assigned"
            })
            warehouses.loc[warehouses['warehouse_id'] == suitable_warehouse['warehouse_id'], 'stock'] -= order['quantity']
        else:
            assignments.append({
                "order_id": order['order_id'],
                "warehouse_id": None,
                "distance_km": None,
                "status": "Unassigned"
            })

    result_df = pd.DataFrame(assignments)
    st.subheader("Fulfillment Results")
    st.dataframe(result_df)

    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Results CSV", csv, "assignments.csv", "text/csv")

