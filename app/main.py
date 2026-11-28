import json
import logging
import sys
from pathlib import Path
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field
from src.bikeprice.logging_utils import logger
MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "model.joblib"


# ---------- JSON logging (stdout only) ----------
class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        extra = getattr(record, "fields", None)
        if extra:
            payload.update(extra)
        return json.dumps(payload)


logger = logging.getLogger("mp295")
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.propagate = False


# ---------- request / response schema ----------
class BikeRequest(BaseModel):
    age_years: float = Field(..., ge=0)
    km_driven: int = Field(..., ge=500)          # client rule 2
    engine_cc: int = Field(..., gt=0)
    owners: int = Field(..., ge=0)
    service_records: int = Field(..., ge=0, le=35)  # client rule 1
    accidents: int = Field(..., ge=0)
    brand_tier: Literal["budget", "mid", "premium"]
    city_zone: Literal["North", "South", "Central"]


class PredictionResponse(BaseModel):
    prediction: float


# ---------- app ----------
app = FastAPI(title="MP295 Two-Wheeler Price API")
_model = None


def get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(req: BikeRequest):
    X = pd.DataFrame([req.model_dump()])
    pred = float(get_model().predict(X)[0])
    logger.info(
        "prediction served",
        extra={"fields": {"event": "predict", "prediction": round(pred, 3),
                          "brand_tier": req.brand_tier, "city_zone": req.city_zone}},
    )
    return PredictionResponse(prediction=pred)