# Vendor Performance Intelligence

An AI-powered system for evaluating and ranking vendor proposals. It uses a machine learning model trained on vendor attributes to generate a performance score, helping procurement teams make data-driven decisions.

## Features

- Score individual or batch vendor proposals via a REST API
- Interactive frontend to add vendors manually or upload a CSV
- AI-ranked comparison with recommendations (Highly Recommended / Recommended / Not Recommended)
- Jupyter notebook for model training and exploration

## How It Works

The ML model scores vendors (0–100) based on a weighted combination of:

| Feature                       | Weight |
| ----------------------------- | ------ |
| Quality Score                 | 25%    |
| On-Time Delivery Rate         | 20%    |
| Unit Price (lower is better)  | 20%    |
| Defect Rate (lower is better) | 15%    |
| Vendor Experience             | 10%    |
| Support Rating                | 10%    |

## Project Structure

```
├── app.py                  # Streamlit frontend
├── backend/
│   └── main.py             # FastAPI backend
├── data/
│   ├── generate_dataset.py # Synthetic dataset generator
│   └── vendor_proposals.csv
├── models/
│   ├── vendor_model.pkl    # Trained ML model
│   ├── scaler.pkl          # Feature scaler
│   └── features.pkl        # Feature list
├── notebooks/
│   └── 01_vendor_ml.ipynb  # Model training notebook
```

## Getting Started

### 1. Activate Virtual Environment

```powershell
vpi\Scripts\Activate.ps1
```

### 2. Run the Backend

```bash
cd backend
uvicorn main:app --reload
```

API: `http://localhost:8000`  
Docs: `http://localhost:8000/docs`

### 3. Run the Frontend

```bash
streamlit run app.py
```

### 4. Run the Notebook

```bash
jupyter notebook
```

Open `notebooks/01_vendor_ml.ipynb` to explore or retrain the model.

## API Endpoints

| Method | Endpoint         | Description            |
| ------ | ---------------- | ---------------------- |
| GET    | `/`              | Health check           |
| POST   | `/predict`       | Score a single vendor  |
| POST   | `/predict_batch` | Score multiple vendors |

### Example Request

```json
POST /predict
{
  "unit_price": 12000,
  "quality_score": 8.5,
  "delivery_days": 20,
  "defect_rate_percent": 2.1,
  "vendor_experience_years": 10,
  "support_rating": 4.2,
  "on_time_delivery_rate": 0.95,
  "certifications_count": 5,
  "payment_terms_days": 30,
  "warranty_months": 24,
  "vendor_region_Europe": 1,
  "vendor_region_Asia": 0,
  "vendor_region_North America": 0,
  "vendor_region_Local": 0,
  "product_category_Electronics": 1,
  "product_category_Machinery": 0,
  "product_category_Software": 0
}
```

### Example Response

```json
{
  "vendor_score": 74.32
}
```

## CSV Upload Format

The frontend supports bulk vendor import via CSV. Required columns:

`unit_price`, `delivery_days`, `quality_score`, `vendor_experience_years`, `defect_rate_percent`, `support_rating`, `on_time_delivery_rate`, `certifications_count`, `payment_terms_days`, `warranty_months`, `vendor_region`, `product_category`

A sample dataset is available at `data/vendor_proposals.csv`.
