from pydantic import BaseModel,Field,field_validator,model_validator
from typing import Annotated
from enum import Enum


class Gender(str,Enum):
    Male = "Male"
    Female = "Female"

class Senior(int,Enum):
    Zero = "0"
    One = "1"

class partner(str,Enum):
    Yes = "Yes"
    No = "No"

class dependent(str,Enum):
    Yes = "Yes"
    No = "No"

class phoneservice(str,Enum):
    Yes = "Yes"
    No = "No"

class multipleline(str,Enum):
    Yes = "Yes"
    No = "No"

class internetservice(str,Enum):
    DSL = "DSL"
    FiberOptic = "Fiber optic"
    No = "No"

class onlinesecurity(str,Enum):
    Yes = "Yes"
    NoService = "No internet service"
    No = "No"

class onlinebackup(str,Enum):
    Yes = "Yes"
    NoService = "No internet service"
    No = "No"

class deviceprotection(str,Enum):
    Yes = "Yes"
    NoService = "No internet service"
    No = "No"

class techsupport(str,Enum):
    Yes = "Yes"
    NoService = "No internet service"
    No = "No"

class streamingtv(str,Enum):
    Yes = "Yes"
    NoService = "No internet service"
    No = "No"

class streamingmovie(str,Enum):
    Yes = "Yes"
    NoService = "No internet service"
    No = "No"

class contract(str,Enum):
    Month = "Month-to-month"
    one_year = "One year"
    two_year = "Two year"

class paperlessbilling(str,Enum):
    Yes = "Yes"
    No = "No"

class paymentmethod(str,Enum):
    Electronic_check = "Electronic check"
    Mailed_check = "Mailed check"
    Bank_transfer = "Bank transfer (automatic)"
    Credit_card = "Credit card (automatic)"


class CustomerFeatures(BaseModel):
    gender: Gender

    SeniorCitizen: Senior

    Partner: partner

    Dependents: dependent

    tenure: Annotated[
        int,Field(ge=0,le=100)
    ]

    PhoneService: phoneservice

    MultipleLines: multipleline

    InternetService: internetservice

    OnlineSecurity: onlinesecurity

    OnlineBackup: onlinebackup

    DeviceProtection: deviceprotection

    TechSupport: techsupport

    StreamingTV: streamingtv

    StreamingMovies: streamingmovie

    Contract: contract

    PaperlessBilling: paperlessbilling

    PaymentMethod: paymentmethod

    MonthlyCharges: Annotated[
        float,Field(ge=0)
        ]

    TotalCharges: Annotated[
        float,Field(ge=0)
        ]
    
    @model_validator(mode='after')
    @classmethod
    def validation(cls,value):

        expected_total = value.MonthlyCharges * value.tenure
        if value.TotalCharges < expected_total * 0.3:
            raise ValueError("TotalCharges value seems unrealistic")
        
        if value.SeniorCitizen == 1 and value.tenure < 1:
            raise ValueError("Invalid senior citizen data")
        
        
        if value.InternetService.value == "No":
            internet_features = [
                value.OnlineSecurity,
                value.OnlineBackup,
                value.DeviceProtection,
                value.TechSupport,
                value.StreamingTV,
                value.StreamingMovies
            ]
            if any(feature != "No internet service" for feature in internet_features):
                raise ValueError("Internet-related services invalid")
            
        if value.MonthlyCharges > value.TotalCharges:
            raise ValueError(
                "TotalCharges cannot be less than MonthlyCharges"
            )
        if value.tenure > 0 and value.TotalCharges == 0:
            raise ValueError(
                "Customer with tenure cannot have zero charges"
            )
                
        return value
    

class PredictionResponse(BaseModel):

    Prediction: str

    Confidence: float

    RiskLevel : str
