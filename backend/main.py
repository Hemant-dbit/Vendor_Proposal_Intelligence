from fastapi import FastAPI
import joblib
import numpy as np
import pandas as pd

app = FastAPI()

# Load model artifacts
model = joblib.load("../models/vendor_model.pkl")
scaler = joblib.load("../models/scaler.pkl")
features = joblib.load("../models/features.pkl")

@app.get("/")
def home():
  return {"message": "Vendor ML API is running"}

@app.post("/predict")
def predict(data: dict):
  df = pd.DataFrame([data])

# One-hot encoding (must match training)
  df = pd.get_dummies(df)

    # Align columns
  df = df.reindex(columns=features, fill_value=0)

    # Scale
  df[df.columns] = scaler.transform(df[df.columns])

    # Predict
  score = model.predict(df)[0]

  return {
        "vendor_score": float(score)
  }

    