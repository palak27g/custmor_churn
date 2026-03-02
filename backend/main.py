from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import logging
import shap
import numpy as np



# --------------------------------------------------
# Logging Configuration
# --------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --------------------------------------------------
# App Initialization
# --------------------------------------------------
app = FastAPI(title="Customer Churn Prediction API")

# --------------------------------------------------
# Load Model + Training Columns
# --------------------------------------------------
try:
    model = joblib.load("model/churn_model_xgboost.pkl")
    model_columns = joblib.load("model/model_columns.pkl")
    logger.info("Model and columns loaded successfully.")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    raise RuntimeError("Model could not be loaded.")

# --------------------------------------------------
# Input Schema
# IMPORTANT:
# Add fields based on your dataset features
# --------------------------------------------------
class CustomerData(BaseModel):
    tenure: int
    MonthlyCharges: float
    TotalCharges: float
    Contract: str
    InternetService: str
    PaymentMethod: str
    OnlineSecurity: str
    TechSupport: str
    PaperlessBilling: str

# --------------------------------------------------
# Health Check
# --------------------------------------------------
@app.get("/")
def health_check():
    return {"status": "API is running successfully"}

# --------------------------------------------------
# Prediction Endpoint
# --------------------------------------------------
@app.post("/predict")
def predict(data: CustomerData):
    try:
        # Convert input to DataFrame
        input_df = pd.DataFrame([data.dict()])
        
        logger.info(f"Received input: {input_df.to_dict()}")

        # One-hot encoding (same as training)
        input_df = pd.get_dummies(input_df)

        # Align with training columns
        input_df = input_df.reindex(columns=model_columns, fill_value=0)

        # Predict probability
        churn_probability = model.predict_proba(input_df)[:, 1][0]

        # Risk Bucketing
        if churn_probability >= 0.6:
            risk = "High Risk"
        elif churn_probability >= 0.45:
            risk = "Medium Risk"
        else:
            risk = "Low Risk"

        logger.info(f"Prediction successful. Probability: {churn_probability}")

        return {
            "churn_probability": round(float(churn_probability), 4),
            "risk_category": risk
        }

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed.")
booster = model.get_booster()

