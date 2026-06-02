from fastapi import FastAPI,HTTPException
import pandas as pd
from src.predict import predict_data,predict_probability
from app.API.schema.customer_schema import CustomerFeatures,PredictionResponse
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="Customer Churn Prediction",description="Predict whether a telecom customer will churn or not")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"messege":"Start Predicting Whether Customer Churn Or Not"}



@app.post("/predict",response_model=PredictionResponse)
def Predict_Customer_Churn(data:CustomerFeatures):
    try:
        input_info = pd.DataFrame([data.model_dump()])
        prediction = predict_data(input_info)
        probability = predict_probability(input_info)
        result = probability[0][1]

        if result >= 0.70:

            output = "Customer Will Churn"
            risk = "High Risk"

        elif result >= 0.40:

            output = "Customer Will Churn"
            risk = "Medium Risk"

        else:

            output = "Customer Will Stay"
            risk = "Low Risk"

        return {
            "Prediction": output,
            "Confidence": round(result * 100, 2),
            "RiskLevel": risk
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )