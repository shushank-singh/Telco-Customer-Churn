from src.data_loader import load_data

from src.train import train_model


df = load_data(
    "data/raw_data/telco_customer_churn_raw.csv"
)

train_model(df)

print("Model Trained Successfully")