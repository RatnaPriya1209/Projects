import streamlit as st
import plotly.express as px
from forecast_model import train_prophet
from mongo_utils import save_forecast_to_mongo
from prepare_data import load_and_merge_data
import pandas as pd

# Setup
st.set_page_config(layout="wide")
st.title("Supply Chain Sales Dashboard")

# Load data
df = load_and_merge_data()
store_ids = df['Store'].unique()
dept_ids = df['Dept'].unique()

# Sidebar filters
st.sidebar.header("Filters")
selected_store = st.sidebar.selectbox("Select Store", store_ids)
selected_dept = st.sidebar.selectbox("Select Department", dept_ids)

# Filter data
filtered = df[(df['Store'] == selected_store) & (df['Dept'] == selected_dept)]

# Sales Trend
st.subheader(f"Weekly Sales for Store {selected_store} - Dept {selected_dept}")
fig = px.line(
    filtered, x='Date', y='Weekly_Sales',
    title="Sales Trend",
    labels={'Date': 'Date', 'Weekly_Sales': 'Weekly Sales'}
)
st.plotly_chart(fig, use_container_width=True)

# Forecast section
st.subheader("Forecast (Next 90 Days)")
forecast = train_prophet(selected_store, selected_dept)
forecast_data = forecast.to_dict(orient="records")

# Save forecast to MongoDB
try:
    save_forecast_to_mongo(forecast_data, selected_store, selected_dept)
    st.success("Forecast data stored in MongoDB.")
except Exception as e:
    st.error(f"MongoDB Error: {e}")

# Forecast chart
fig2 = px.line(forecast, x="ds", y="yhat", title="Forecast Sales")
fig2.add_scatter(x=forecast['ds'], y=forecast['yhat_upper'], mode='lines', name='Upper Bound', line=dict(dash='dash'))
fig2.add_scatter(x=forecast['ds'], y=forecast['yhat_lower'], mode='lines', name='Lower Bound', line=dict(dash='dash'))
st.plotly_chart(fig2, use_container_width=True)

# Markdown analysis
st.subheader("Markdown Impact")
markdown_cols = [col for col in filtered.columns if "MarkDown" in col]
if markdown_cols:
    st.bar_chart(filtered[markdown_cols].mean())
else:
    st.info("No Markdown data available for this selection.")
