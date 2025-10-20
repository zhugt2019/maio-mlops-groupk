# src/train.py
import argparse
import joblib

# import pandas as pd
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split

# from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, RidgeCV

# from sklearn.ensemble import GradientBoostingRegressor
# from sklearn.model_selection import GridSearchCV
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


# def build_model(model_type="linear"):
#     """构建 scikit-learn 模型"""
#     if model_type == "linear":
#         model = LinearRegression()  # v0.1
#     elif model_type == "rf":
#         model = RandomForestRegressor(
#             n_estimators=100, random_state=SEED, n_jobs=-1
#         )  # v0.2
#     else:
#         raise ValueError("无效的模型类型")
#     return model


# def build_model(model_type="linear"):
#     """构建 scikit-learn 模型"""
#     if model_type == "linear":
#         model = LinearRegression()  # v0.1
#     elif model_type == "rf":
#         model = RandomForestRegressor(
#             n_estimators=100,
#             random_state=SEED,
#             n_jobs=-1,
#             max_depth=10
#         )  # v0.2
#     else:
#         raise ValueError("无效的模型类型")
#     return model

# def build_model(model_type="linear"):
#     """构建 scikit-learn 模型"""
#     if model_type == "linear":
#         model = LinearRegression()  # v0.1

#     elif model_type == "rf":
#         #
#         # 我们使用 RidgeCV 来自动找到最佳的 alpha (正则化强度)
#         #
#         print("注意：使用 RidgeCV (交叉验证) 作为 v0.2 模型")

#         # 定义一系列要尝试的 alpha 值
#         alphas_to_try = [0.01, 0.1, 0.5, 1.0, 5.0, 10.0]

#         # RidgeCV 将自动在训练数据上使用交叉验证来找到最佳 alpha
#         model = RidgeCV(alphas=alphas_to_try) # v0.2

#     else:
#         raise ValueError("无效的模型类型")
#     return model


def build_model(model_type="linear"):
    """构建 scikit-learn 模型"""
    if model_type == "linear":
        model = LinearRegression()  # v0.1

    elif model_type == "rf":
        #
        # 我们使用 RidgeCV 来自动找到最佳的 alpha (正则化强度)
        #
        print("注意：使用 RidgeCV (交叉验证) 作为 v0.2 模型")

        # 定义一系列要尝试的 alpha 值
        alphas_to_try = [0.01, 0.1, 0.5, 1.0, 5.0, 10.0]

        # RidgeCV 将自动在训练数据上使用交叉验证来找到最佳 alpha
        model = RidgeCV(alphas=alphas_to_try)  # v0.2

    else:
        raise ValueError("无效的模型类型")
    return model


# def build_model(model_type="linear"):
#     """构建 scikit-learn 模型"""
#     if model_type == "linear":
#         model = LinearRegression()  # v0.1

#     elif model_type == "rf":
#         print("注意：使用 GradientBoostingRegressor 作为 v0.2 模型")
#         model = GradientBoostingRegressor(random_state=SEED, n_estimators=150, max_depth=3, learning_rate=0.1)

#     else:
#         raise ValueError("无效的模型类型")
#     return model

# def build_model(model_type="linear"):
#     """构建 scikit-learn 模型"""
#     if model_type == "linear":
#         model = LinearRegression()  # v0.1

#     elif model_type == "rf":
#         print("注意：使用 GridSearchCV(RandomForest) 作为 v0.2 模型")
#         # 定义要搜索的参数网格
#         param_grid = {
#             'n_estimators': [100, 200],
#             'max_depth': [5, 10, 15],
#             'min_samples_leaf': [1, 2, 4]
#         }
#         rf = RandomForestRegressor(random_state=SEED, n_jobs=-1)

#         # cv=3 意味着 3 折交叉验证
#         model = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, scoring='neg_mean_squared_error')

#     else:
#         raise ValueError("无效的模型类型")
#     return model

# def train(version):
#     """训练、评估并保存指定版本的模型"""
#     print("正在加载数据...")
#     X_train, X_test, y_train, y_test = load_data()

#     model_type = "linear" if version == "v0.1" else "rf"

#     print(f"正在为 {version} ({model_type}) 构建模型...")
#     model = build_model(model_type)

#     print("正在训练模型...")
#     model.fit(X_train, y_train)

#     preds = model.predict(X_test)
#     rmse = np.sqrt(mean_squared_error(y_test, preds))

#     print(f"--- 模型 {version} ---")
#     print(f"模型类型: {model_type}")
#     print(f"测试集 RMSE: {rmse:.4f}")
#     print("---------------------")

#     model_path = os.path.join(MODEL_DIR, f"model-{version}.joblib")
#     joblib.dump(model, model_path)
#     print(f"模型已保存至 {model_path}")
#     print("重要提示：请将 'models/' 目录下的 .joblib 文件提交到 Git。")


def train(version):
    """训练、评估并保存指定版本的模型"""
    print("正在加载数据...")
    X_train, X_test, y_train, y_test = load_data()

    model_type = "linear" if version == "v0.1" else "rf"

    print(f"正在为 {version} ({model_type}) 构建模型...")
    model = build_model(model_type)

    print("正在训练模型...")
    model.fit(X_train, y_train)

    # --- 开始诊断修改 ---

    # 1. 在测试集 (Test Set) 上评估
    test_preds = model.predict(X_test)
    test_rmse = np.sqrt(mean_squared_error(y_test, test_preds))

    # 2. 在训练集 (Train Set) 上评估
    train_preds = model.predict(X_train)
    train_rmse = np.sqrt(mean_squared_error(y_train, train_preds))

    # --- 结束诊断修改 ---

    print(f"--- 模型 {version} ---")
    print(f"模型类型: {model_type}")

    # --- 开始打印修改 ---
    print(f"训练集 RMSE (Train RMSE): {train_rmse:.4f}")
    print(f"测试集 RMSE (Test RMSE): {test_rmse:.4f}")
    # --- 结束打印修改 ---

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
        help="要训练的模型版本 (v0.1 或 v0.2)",
    )
    args = parser.parse_args()
    train(args.version)
