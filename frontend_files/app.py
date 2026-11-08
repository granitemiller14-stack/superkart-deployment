import os
import requests
import pandas as pd
import streamlit as st

# Address of the Flask backend (container name on the Docker network)
API_URL = os.getenv("API_URL", "http://superkart-backend:7860")

st.title("SuperKart Sales Prediction")

# ---------- Single prediction ----------
st.subheader("Predict sales for one product")

product_weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
sugar_content = st.selectbox("Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
allocated_area = st.number_input("Allocated Display Area (ratio)", min_value=0.0, max_value=1.0, value=0.027, format="%.3f")
product_mrp = st.number_input("Product MRP", min_value=0.0, value=117.08)
store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
city_type = st.selectbox("City Type", ["Tier 1", "Tier 2", "Tier 3"])
store_type = st.selectbox("Store Type", ["Departmental Store", "Supermarket Type1", "Supermarket Type2", "Food Mart"])
product_id_char = st.selectbox("Product Category Code", ["FD", "NC", "DR"])
store_age = st.number_input("Store Age (years)", min_value=0, value=16)
type_category = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])

if st.button("Predict"):
    payload = {
        "Product_Weight": product_weight,
        "Product_Sugar_Content": sugar_content,
        "Product_Allocated_Area": allocated_area,
        "Product_MRP": product_mrp,
        "Store_Size": store_size,
        "Store_Location_City_Type": city_type,
        "Store_Type": store_type,
        "Product_Id_char": product_id_char,
        "Store_Age_Years": store_age,
        "Product_Type_Category": type_category,
    }
    response = requests.post(f"{API_URL}/v1/predict", json=payload)
    if response.status_code == 200:
        st.success(f"Predicted Sales: {response.json()['Predicted_Sales']}")
    else:
        st.error("Prediction failed. Check that the backend is running.")

# ---------- Batch prediction ----------
st.subheader("Predict sales for a CSV file")

uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file is not None and st.button("Predict Batch"):
    response = requests.post(f"{API_URL}/v1/predictbatch", files={"file": uploaded_file.getvalue()})
    if response.status_code == 200:
        st.write(response.json())
    else:
        st.error("Batch prediction failed. Check that the backend is running.")
