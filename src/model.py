# src/model.py
import joblib
import pandas as pd
import os
from .schemas import PredictionRequest
import logging

logger = logging.getLogger(__name__)


class Model:
    def __init__(self, model_path: str, version: str):
        if not os.path.exists(model_path):
            logger.error(f"模型文件未在 {model_path} 找到")
            raise FileNotFoundError(f"模型文件未在 {model_path} 找到")
        self.model = joblib.load(model_path)
        self.version = version
        logger.info(f"模型 {version} ({model_path}) 加载成功")

    def predict(self, data: PredictionRequest) -> float:
        df = pd.DataFrame([data.model_dump()])
        prediction = self.model.predict(df)
        return float(prediction[0])


# --- 全局模型加载 ---
MODEL_VERSION = os.getenv("MODEL_VERSION", "v0.1")
# Docker 容器内的路径
MODEL_PATH = f"/app/models/model-{MODEL_VERSION}.joblib"

model: Model | None = None


def load_model():
    """在应用启动时加载全局模型实例"""
    global model
    try:
        model = Model(model_path=MODEL_PATH, version=MODEL_VERSION)
    except FileNotFoundError:
        logger.error(f"启动失败：无法加载模型 {MODEL_VERSION}")
        model = None


def get_model() -> Model:
    """FastAPI 依赖项，用于获取已加载的模型"""
    if model is None:
        raise RuntimeError(f"模型 {MODEL_VERSION} 未加载。")
    return model
