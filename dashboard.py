import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="AI Automation Dashboard", layout="wide")

# Title
st.title("🚀 AI Automation Dashboard")

# Upload Excel
st.sidebar.header("Upload Excel File")
file = st.sidebar.file_uploader("Upload sales file", type=["csv", "xlsx"])

if file:
    df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
else:
    # Default Sample Data
    df = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr"],
        "Sales": [100, 200, 150, 300],
        "Profit": [10, 40, 30, 60]
    })

# KPI Cards
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", total_sales)
col2.metric("📈 Total Profit", total_profit)
col3.metric("📊 Records", len(df))

# Main Layout
left, right = st.columns(2)

# LEFT: Table
with left:
    st.subheader("📋 Data Table")
    st.dataframe(df)

# RIGHT: Chart
with right:
    st.subheader("📊 Sales Chart")
    fig, ax = plt.subplots()
    ax.plot(df["Month"], df["Sales"], marker="o")
    st.pyplot(fig)

# Bottom Section
col4, col5 = st.columns(2)

# Add Data Form
with col4:
    st.subheader("➕ Add New Entry")
    month = st.text_input("Month")
    sales = st.number_input("Sales", 0)
    profit = st.number_input("Profit", 0)

    if st.button("Add Data"):
        new_row = {"Month": month, "Sales": sales, "Profit": profit}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        st.success("Added Successfully!")

# AI Prediction
with col5:
    st.subheader("🤖 AI Sales Prediction")

    if len(df) >= 2:
        X = [[i] for i in range(len(df))]
        y = df["Sales"]

        model = LinearRegression()
        model.fit(X, y)

        next_month = st.number_input("Predict for next Month Number", len(df)+1)
        prediction = model.predict([[next_month]])
        st.write(f"🔮 Predicted Sales = {int(prediction[0])}")

# Settings
st.sidebar.header("⚙️ Settings")
theme = st.sidebar.selectbox("Theme", ["Light", "Dark"])
refresh = st.sidebar.slider("Auto Refresh (sec)", 1, 10, 5)

st.sidebar.info("AI Automation Dashboard Running...")