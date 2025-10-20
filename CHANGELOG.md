# Changelog

本文档记录了该项目的所有显著变更。

## [v0.2] - [YYYY-MM-DD]  <-- (当你发布 v0.2 时在此处填写)

### 变更
* **模型:** 从 `LinearRegression` (v0.1) 升级到 `RandomForestRegressor` (v0.2)。
* **理由:** `RandomForestRegressor` 能够捕捉特征之间更复杂的非线性关系，从而显著降低预测误差 (RMSE)。

### 性能指标
| 版本 | 模型 | 测试集 RMSE |
| :--- | :--- | :--- |
| **v0.2** | `RandomForestRegressor` | **48.8687** |
| **v0.1** | `LinearRegression` | **53.8869** |

* **改进:** RMSE 降低了 5.0182 (约 9.3%)。
* **Rationale:**  
The Random Forest model in **v0.2** captures nonlinear relationships between features and target values that the linear model in **v0.1** could not represent.  
By combining multiple decision trees and averaging their outputs, it reduces variance and improves generalization.  
As a result, v0.2 achieves a lower RMSE (53.8869 vs 48.8687), confirming a tangible improvement in prediction accuracy and model robustness.

---

## [v0.1] - [YYYY-MM-DD]  <-- (在此处填写今天的日期)

### 变更
* **初始版本:**
* **模型:** `LinearRegression` (在已缩放数据上训练)。
* **API:** 建立基础 API，包含 `/health` 和 `/predict` 端点。
* **CI/CD:** 建立基础的 CI (lint, build-test) 和 Release (push-to-ghcr, smoke-test, create-release) 流程。
* **指标:** 基线测试集 RMSE: 53.8869。
