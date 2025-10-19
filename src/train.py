# src/train.py
import argparse
import joblib
import pandas as pd
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
import os

# 为可复现性设置随机种子
SEED = 2025
np.random.seed(SEED)

# 路径是相对于仓库根目录的
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

def load_data():
    """加载并拆分 diabetes 数据集"""
    data = load_diabetes(as_frame=True)
    X = data.frame.drop(columns=["target"])
    y = data.frame["target"]
    # 
    # 修正 #1：根据教授的澄清，数据已缩放
    # 我们不再使用 StandardScaler
    #
    return train_test_split(X, y, test_size=0.2, random_state=SEED)

def build_model(model_type="linear"):
    """构建 scikit-learn 模型"""
    if model_type == "linear":
        model = LinearRegression() # v0.1
    elif model_type == "rf":
        model = RandomForestRegressor(n_estimators=100, random_state=SEED, n_jobs=-1) # v0.2
    else:
        raise ValueError("无效的模型类型")
        
    return model

def train(version):
    """训练、评估并保存指定版本的模型"""
    print(f"正在加载数据...")
    X_train, X_test, y_train, y_test = load_data()
    
    model_type = "linear" if version == "v0.1" else "rf"
        
    print(f"正在为 {version} ({model_type}) 构建模型...")
    model = build_model(model_type)
    
    print("正在训练模型...")
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    
    print(f"--- 模型 {version} ---")
    print(f"模型类型: {model_type}")
    print(f"测试集 RMSE: {rmse:.4f}")
    print("---------------------")
    
    model_path = os.path.join(MODEL_DIR, f"model-{version}.joblib")
    joblib.dump(model, model_path)
    print(f"模型已保存至 {model_path}")
    print("重要提示：请将 'models/' 目录下的 .joblib 文件提交到 Git。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="本地训练糖尿病进展模型")
    parser.add_argument(
        "--version", 
        type=str, 
        required=True, 
        choices=["v0.1", "v0.2"],
        help="要训练的模型版本 (v0.1 或 v0.2)"
    )
    args = parser.parse_args()
    train(args.version)