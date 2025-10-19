# src/app.py
from fastapi import FastAPI, Depends, HTTPException

# 使用相对导入，因为我们在 'src' 模块内
from .schemas import PredictionRequest, PredictionResponse, HealthResponse
from .model import get_model, load_model, Model
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Diabetes Progression API", version="0.2.0")


@app.on_event("startup")
def startup_event():
    load_model()


@app.get("/health", response_model=HealthResponse)
def health_check():
    """返回模型版本和状态"""
    try:
        model_instance = get_model()
        return {"status": "ok", "model_version": model_instance.version}
    except RuntimeError:
        return {
            "status": "error: model not loaded",
            "model_version": os.getenv("MODEL_VERSION", "unknown"),
        }


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest, model: Model = Depends(get_model)):
    """接收已缩放的患者特征并返回进展风险评分"""
    try:
        prediction = model.predict(request)
        return {"prediction": prediction}
    except Exception as e:
        logger.error(f"预测失败: {e}")
        raise HTTPException(status_code=500, detail=f"预测失败。错误: {str(e)}")
