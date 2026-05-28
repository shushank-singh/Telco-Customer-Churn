import pandas as pd

from sklearn.preprocessing import (
    StandardScaler,
    OneHotEncoder
)

from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline

from sklearn.impute import SimpleImputer

def preprocess_data(df):

    df["TotalCharges"] = pd.to_numeric(
        df["TotalCharges"],
        errors="coerce"
    )

    df.drop(columns=["customerID"], inplace=True)

    numerical_col = df.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    categorical_col = df.select_dtypes(
        include=["object"]
    ).columns.tolist()

    if "Churn" in categorical_col:
        categorical_col.remove("Churn")

    numerical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="mean")),
        ("scaler", StandardScaler())
    ])
    categorical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numerical_pipeline, numerical_col),
            ("cat", categorical_pipeline, categorical_col)
        ]
    )

    return preprocessor
    