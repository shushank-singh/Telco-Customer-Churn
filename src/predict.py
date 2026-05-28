import joblib
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "final_model.pkl"
)

model = joblib.load(MODEL_PATH)

def predict_data(data):

    prediction = model.predict(data)

    return prediction


def predict_probability(data):
    
    prob = model.predict_proba(data)

    return prob