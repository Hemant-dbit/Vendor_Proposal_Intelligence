import argparse
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib


def generate_dataset(N, out_path):
    np.random.seed(42)

    experience = np.random.randint(1, 31, N)
    quality_base = 3 + (experience / 30) * 5
    quality_score = np.clip(quality_base + np.random.normal(0, 1.2, N), 1, 10)
    unit_price = np.clip(5000 + quality_score * 3000 + np.random.normal(0, 4000, N), 500, 50000)
    delivery_base = 60 - (experience / 30) * 30
    delivery_days = np.clip(delivery_base + np.random.normal(0, 12, N), 1, 90).astype(int)
    defect_rate = np.clip(12 - quality_score * 0.9 + np.random.normal(0, 1.5, N), 0.1, 15)
    support_base = 2 + (experience / 30) * 2.5
    support_rating = np.clip(support_base + np.random.normal(0, 0.6, N), 1, 5)
    on_time_base = 0.5 + (experience / 30) * 0.4 + (1 - defect_rate / 15) * 0.1
    on_time_rate = np.clip(on_time_base + np.random.normal(0, 0.08, N), 0.5, 1.0)
    certifications = np.clip((experience / 30) * 7 + np.random.normal(0, 1.5, N), 0, 10).astype(int)
    payment_terms = np.random.choice([15, 30, 45, 60, 90, 120], N)
    warranty = np.random.choice([0, 6, 12, 24, 36, 48, 60], N)
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

    scaler = MinMaxScaler()
    numeric_cols = df.select_dtypes(include=np.number).columns
    norm = pd.DataFrame(scaler.fit_transform(df[numeric_cols]), columns=numeric_cols)

    df['vendor_score'] = (
        norm['quality_score'] * 0.25 +
        norm['on_time_delivery_rate'] * 0.20 +
        (1 - norm['unit_price']) * 0.20 +
        (1 - norm['defect_rate_percent']) * 0.15 +
        norm['vendor_experience_years'] * 0.10 +
        norm['support_rating'] * 0.10
    ) * 100

    df['vendor_score'] = np.clip(df['vendor_score'] + np.random.normal(0, 2, N), 0, 100)
    df.insert(0, 'vendor_id', [f'V{str(i).zfill(4)}' for i in range(1, N+1)])

    os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Generated dataset with {N} rows -> {out_path}")


def train(data_path, model_dir, random_state=42):
    df = pd.read_csv(data_path)
    if 'vendor_score' not in df.columns:
        raise RuntimeError('vendor_score target column not found in dataset')

    y = df['vendor_score']
    X = df.drop(columns=['vendor_id', 'vendor_score'])
    X = pd.get_dummies(X)

    features = X.columns.tolist()
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=random_state)

    model = RandomForestRegressor(n_estimators=200, random_state=random_state, n_jobs=-1)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    print('Training complete')
    print(f'R2: {r2:.4f}  RMSE: {rmse:.4f}  MAE: {mae:.4f}')

    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(model, os.path.join(model_dir, 'vendor_model.pkl'))
    joblib.dump(scaler, os.path.join(model_dir, 'scaler.pkl'))
    joblib.dump(features, os.path.join(model_dir, 'features.pkl'))

    print(f'Artifacts saved to {model_dir}')


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--samples', type=int, default=None, help='If set, regenerate dataset with this many samples')
    p.add_argument('--data-path', type=str, default='data/vendor_proposals.csv')
    p.add_argument('--model-dir', type=str, default='models')
    p.add_argument('--random-state', type=int, default=42)
    return p.parse_args()


if __name__ == '__main__':
    args = parse_args()

    if args.samples:
        # regenerate dataset if requested
        print(f'Regenerating dataset with N={args.samples}')
        generate_dataset(args.samples, args.data_path)

    if not os.path.exists(args.data_path):
        raise SystemExit(f'Dataset not found at {args.data_path}. Run with --samples to generate one.')

    train(args.data_path, args.model_dir, random_state=args.random_state)
