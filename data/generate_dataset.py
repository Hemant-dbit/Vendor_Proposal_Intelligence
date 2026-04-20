import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

np.random.seed(42)

N = 400  # number of vendors

# Experience
experience = np.random.randint(1, 31, N)

# Quality depends on experience
quality_base = 3 + (experience / 30) * 5
quality_score = np.clip(quality_base + np.random.normal(0, 1.2, N), 1, 10)

# Price depends on quality
unit_price = np.clip(5000 + quality_score * 3000 + np.random.normal(0, 4000, N), 500, 50000)

# Delivery time improves with experience
delivery_base = 60 - (experience / 30) * 30
delivery_days = np.clip(delivery_base + np.random.normal(0, 12, N), 1, 90).astype(int)

# Defects inverse of quality
defect_rate = np.clip(12 - quality_score * 0.9 + np.random.normal(0, 1.5, N), 0.1, 15)

# Support rating
support_base = 2 + (experience / 30) * 2.5
support_rating = np.clip(support_base + np.random.normal(0, 0.6, N), 1, 5)

# On-time delivery
on_time_base = 0.5 + (experience / 30) * 0.4 + (1 - defect_rate / 15) * 0.1
on_time_rate = np.clip(on_time_base + np.random.normal(0, 0.08, N), 0.5, 1.0)

# Certifications
certifications = np.clip((experience / 30) * 7 + np.random.normal(0, 1.5, N), 0, 10).astype(int)

# Payment terms
payment_terms = np.random.choice([15, 30, 45, 60, 90, 120], N)

# Warranty
warranty = np.random.choice([0, 6, 12, 24, 36, 48, 60], N)

# Categories
regions = np.random.choice(['Asia', 'Europe', 'North America', 'Local'], N)
categories = np.random.choice(['Electronics', 'Raw Materials', 'Packaging', 'Machinery', 'IT Services'], N)

df = pd.DataFrame({
    'unit_price': unit_price,
    'delivery_days': delivery_days,
    'quality_score': quality_score,
    'vendor_experience_years': experience,
    'defect_rate_percent': defect_rate,
    'support_rating': support_rating,
    'on_time_delivery_rate': on_time_rate,
    'certifications_count': certifications,
    'payment_terms_days': payment_terms,
    'warranty_months': warranty,
    'vendor_region': regions,
    'product_category': categories,
})

# Normalize
scaler = MinMaxScaler()
numeric_cols = df.select_dtypes(include=np.number).columns
norm = pd.DataFrame(scaler.fit_transform(df[numeric_cols]), columns=numeric_cols)

# Target (MOST IMPORTANT)
df['vendor_score'] = (
    norm['quality_score'] * 0.25 +
    norm['on_time_delivery_rate'] * 0.20 +
    (1 - norm['unit_price']) * 0.20 +
    (1 - norm['defect_rate_percent']) * 0.15 +
    norm['vendor_experience_years'] * 0.10 +
    norm['support_rating'] * 0.10
) * 100

# Add noise
df['vendor_score'] = np.clip(df['vendor_score'] + np.random.normal(0, 2, N), 0, 100)

# Vendor ID
df.insert(0, 'vendor_id', [f'V{str(i).zfill(3)}' for i in range(1, N+1)])

# Save
df.to_csv('vendor_proposals.csv', index=False)

print("Dataset created successfully!")
print(df.head())