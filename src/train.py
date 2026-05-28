import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from imblearn.pipeline import Pipeline
import joblib
from src.preprocessing import preprocess_data
from imblearn.over_sampling import SMOTE

def train_model(df):

    df["TotalCharges"] = pd.to_numeric(
        df["TotalCharges"],
        errors="coerce"
    )

    X = df.drop("Churn", axis=1)
    y = df["Churn"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    preprocessor = preprocess_data(df)

    model_pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("smote",SMOTE(random_state=42)),
        ("model", LogisticRegression(
            class_weight="balanced",
            random_state=42,
            max_iter=1000
        ))
    ])

    model_pipeline.fit(X_train, y_train)

    joblib.dump(model_pipeline, "models/final_model.pkl")

    return model_pipeline, X_test, y_test