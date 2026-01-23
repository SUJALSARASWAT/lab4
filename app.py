from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

model = joblib.load("model.pkl")

class WineInput(BaseModel):
    features: list

@app.post("/predict")
def predict(data: WineInput):
    features = np.array(data.features).reshape(1, -1)
    prediction = model.predict(features)

    return {
        "name": "Sujal Saraswat",
        "roll_no": "2022BCS0015",
        "wine_quality": int(round(prediction[0]))
    }
