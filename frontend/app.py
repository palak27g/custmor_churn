import streamlit as st
import requests

st.title("Customer Churn Prediction")

tenure = st.slider("Tenure (months)", 0, 72, 24)
monthly = st.number_input("Monthly Charges", value=80.0)
total = st.number_input("Total Charges", value=2000.0)

contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
payment = st.selectbox(
    "Payment Method",
    [
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ]
)

online_security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
tech_support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
paperless = st.selectbox("Paperless Billing", ["Yes", "No"])

if st.button("Predict"):
    payload = {
        "tenure": int(tenure),
        "MonthlyCharges": float(monthly),
        "TotalCharges": float(total),
        "Contract": contract,
        "InternetService": internet,
        "PaymentMethod": payment,
        "OnlineSecurity": online_security,
        "TechSupport": tech_support,
        "PaperlessBilling": paperless
    }

    API_URL = "https://churnx-cipb.onrender.com"

    try:
        with st.spinner("Calling prediction API..."):
            response = requests.post(
                f"{API_URL}/predict",
                json=payload,
                timeout=40
            )

        if response.status_code == 200:
            result = response.json()
            st.success(f"Churn Probability: {result['churn_probability']}")
            st.info(f"Risk Category: {result['risk_category']}")
        else:
            st.error(f"API error: {response.status_code}")
            st.write(response.text)

    except requests.exceptions.RequestException as e:
        st.error("Request failed. Backend may be waking up (free tier cold start).")
        st.write(str(e))