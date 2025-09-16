import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.pyfunc
import os
import random
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MLOps - TP2")

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
MODEL_NAME = os.getenv("MODEL_NAME")
MODEL_VERSION = os.getenv("MODEL_VERSION")

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

current_model = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/{MODEL_VERSION}")
next_model = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/{MODEL_VERSION}")

current_version = MODEL_VERSION
next_version = MODEL_VERSION

CANARY_PROBABILITY = 0.9


class PredictRequest(BaseModel):
    inputs: list


@app.post("/predict")
def predict(request: PredictRequest):
    global current_model, next_model
    try:
        df = pd.DataFrame(request.inputs)

        if random.random() < CANARY_PROBABILITY:
            model = current_model
            used_model = "current"
        else:
            model = next_model
            used_model = "next"

        preds = model.predict(df)
        return {"predictions": preds.tolist(), "used_model": used_model}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class UpdateModelRequest(BaseModel):
    version: str


@app.post("/update-model")
def update_model(req: UpdateModelRequest):
    global next_model, next_version
    try:
        next_model = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/{req.version}")
        next_version = req.version
        return {"status": "success", "new_version": req.version}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/accept-next-model")
def accept_next_model():
    global current_model, next_model, current_version, next_version
    try:
        current_model = next_model
        current_version = next_version

        return {"status": "success", "current_version": current_version}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
