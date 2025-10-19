# src/schemas.py
from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    """
    预测请求的输入特征
    (基于已缩放的 scikit-learn diabetes 数据集)
    """
    age: float
    sex: float
    bmi: float
    bp: float
    s1: float
    s2: float
    s3: float
    s4: float
    s5: float
    s6: float

    class Config:
        json_schema_extra = {
            "example": {
                "age": 0.02,
                "sex": -0.044,
                "bmi": 0.06,
                "bp": -0.03,
                "s1": -0.02,
                "s2": 0.03,
                "s3": -0.02,
                "s4": 0.02,
                "s5": 0.02,
                "s6": -0.001,
            }
        }

class PredictionResponse(BaseModel):
    prediction: float = Field(..., example=150.0)

class HealthResponse(BaseModel):
    status: str = Field(..., example="ok")
    model_version: str = Field(..., example="v0.1")