from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import numpy as np

# Load the trained model at startup
model = joblib.load("model.pkl")

# Initialize FastAPI app
app = FastAPI(
    title="Iris Classifier API",
    version="1.0.0"
)

# Request schema
class PredictionRequest(BaseModel):
    sepal_length: float = Field(..., gt=0, description="Sepal length in cm")
    sepal_width: float = Field(..., gt=0, description="Sepal width in cm")
    petal_length: float = Field(..., gt=0, description="Petal length in cm")
    petal_width: float = Field(..., gt=0, description="Petal width in cm")

# Response schema
class PredictionResponse(BaseModel):
    prediction: int
    confidence: float

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    # Prepare input for model
    features = np.array([[
        request.sepal_length,
        request.sepal_width,
        request.petal_length,
        request.petal_width
    ]])

    # Make prediction
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    confidence = float(max(probabilities))

    return PredictionResponse(
        prediction=int(prediction),
        confidence=confidence
    )


@app.get("/health")
def health():
    return {"status": "ok"}
