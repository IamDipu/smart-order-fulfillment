import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Setup page configuration
st.set_page_config(page_title="Smart Order System", page_icon="📦", layout="centered")

# Connect to DB
conn = sqlite3.connect("orders.db", check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer TEXT,
        product TEXT,
        quantity INTEGER,
        priority TEXT
    )
""")
conn.commit()

# Title and logo
st.markdown("<h1 style='text-align: center;'>📦 Smart Order Fulfillment System</h1>", unsafe_allow_html=True)
st.markdown("### Use the tabs below to Add Orders, View Data, and Analyze Trends.")

# Tab layout
tab1, tab2, tab3 = st.tabs(["➕ Add Order", "📋 View Orders", "📈 Analytics"])

# --- TAB 1: Add Order ---
with tab1:
    st.subheader("➕ Add New Order")

    with st.form("order_form"):
        col1, col2 = st.columns(2)
        with col1:
            customer = st.text_input("👤 Customer Name")
            quantity = st.number_input("🔢 Quantity", min_value=1, value=1)
        with col2:
            product = st.text_input("📦 Product Name")
            priority = st.selectbox("⚡ Priority Level", ["High", "Medium", "Low"])

        submitted = st.form_submit_button("✅ Submit Order")

        if submitted:
            if customer.strip() == "" or product.strip() == "":
                st.warning("⚠️ Please fill in all fields.")
            else:
                cursor.execute("INSERT INTO orders (customer, product, quantity, priority) VALUES (?, ?, ?, ?)",
                               (customer, product, quantity, priority))
                conn.commit()
                st.toast("Order submitted successfully 🎉")
                st.success(f"Order for {customer} added!")

# --- TAB 2: View Orders ---
with tab2:
    st.subheader("📋 All Orders")
    df = pd.read_sql_query("SELECT * FROM orders", conn)

    if df.empty:
        st.info("No orders found. Add some in the 'Add Order' tab.")
    else:
        st.dataframe(df.style.highlight_max(axis=0), use_container_width=True)

# --- TAB 3: Analytics ---
with tab3:
    st.subheader("📈 Order Analytics")

    df = pd.read_sql_query("SELECT * FROM orders", conn)

    if df.empty:
        st.warning("No data available for analysis.")
    else:
        priority_counts = df["priority"].value_counts()

        st.markdown("#### ⚡ Priority Distribution")
        fig, ax = plt.subplots()
        ax.pie(priority_counts, labels=priority_counts.index, autopct='%1.1f%%', startangle=90)
        ax.axis("equal")
        st.pyplot(fig)

        st.markdown("#### 📦 Orders by Product")
        product_counts = df["product"].value_counts()
        st.bar_chart(product_counts)

        st.markdown("#### 👥 Orders by Customer")
        customer_counts = df["customer"].value_counts()
        st.bar_chart(customer_counts)


