import streamlit as st
import requests

st.title("Vendor Proposal Intelligence System")

st.write("Enter vendor details to predict vendor score")

unit_price = st.number_input("Unit Price", 1000, 50000, 10000)
quality_score = st.slider("Quality Score", 1.0, 10.0, 7.0)
delivery_days = st.number_input("Delivery Days", 1, 90, 30)
defect_rate = st.slider("Defect Rate (%)", 0.0, 15.0, 5.0)
experience = st.number_input("Experience (years)", 1, 30, 5)

if st.button("Predict Vendor Score"):

    data = {
        "unit_price": unit_price,
        "quality_score": quality_score,
        "delivery_days": delivery_days,
        "defect_rate_percent": defect_rate,
        "vendor_experience_years": experience,
        "support_rating": 4,
        "on_time_delivery_rate": 0.9,
        "certifications_count": 5,
        "payment_terms_days": 30,
        "warranty_months": 12,
        "vendor_region_Europe": 0,
        "vendor_region_Asia": 1,
        "product_category_Electronics": 1
    }

    response = requests.post("http://localhost:8000/predict", json=data)

    if response.status_code == 200:
        result = response.json()
        st.success(f"Predicted Vendor Score: {result['vendor_score']:.2f}")
    else:
        st.error("Error connecting to API")