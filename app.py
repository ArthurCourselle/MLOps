import joblib
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()
model = joblib.load("regression.joblib")


class HouseFeatures(BaseModel):
    size: float
    nb_rooms: int
    garden: int


@app.post("/predict")
def predict(features: HouseFeatures):
    X = pd.DataFrame([features.dict()])
    y_pred = model.predict(X)[0]
    return {"y_pred": float(y_pred)}
