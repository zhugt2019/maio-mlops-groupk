# maio-mlops-groupk
Assignment3 in MAIO

# 虚拟糖尿病诊所 - 分诊 ML 服务

该服务为糖尿病进展提供风险评分，以帮助虚拟诊所优先安排患者随访。

## 模型版本与性能

| 版本 | 模型 | 测试集 RMSE |
| :--- | :--- | :--- |
| **v0.2** | `RandomForestRegressor` | 48.8687 |
| **v0.1** | `LinearRegression` | 53.8869 |

详细信息请参阅 `CHANGELOG.md`。

## 运行服务 (Docker Compose)

服务通过 GitHub Actions 构建并发布到 GHCR。根据作业 Q&A，请使用 `docker-compose` 来运行服务。

1.  **编辑 `docker-compose.yml`:**
    打开 `docker-compose.yml` 文件。将 `image:` 字段中的 `<ORG>/<REPO>` 替换为你的 GitHub 用户名和仓库名称。

    *示例:*
    ```diff
    - image: ghcr.io/<ORG>/<REPO>:v0.1
    + image: ghcr.io/my-username/my-diabetes-api:v0.1
    ```

2.  **拉取并运行服务:**
    此命令将从 GHCR 拉取 `v0.1` 和 `v0.2` 镜像，并在后台启动它们。
    ```bash
    docker-compose up -d
    ```

3.  **验证服务:**
    * **v0.1** 运行在 `http://localhost:8001`
    * **v0.2** 运行在 `http://localhost:8002`

    检查健康状况：
    ```bash
    curl http://localhost:8001/health
    # 响应: {"status":"ok", "model_version": "v0.1"}
    
    curl http://localhost:8002/health
    # 响应: {"status":"ok", "model_version": "v0.2"}
    ```

4.  **停止服务:**
    ```bash
    docker-compose down
    ```

## API 端点

### 健康检查
`GET /health`

### 预测
`POST /predict`

**示例 (v0.2):**
```bash
curl -X POST http://localhost:8002/predict -H "Content-Type: application/json" -d \
'{
  "age": 0.02, "sex": -0.044, "bmi": 0.06, "bp": -0.03,
  "s1": -0.02, "s2": 0.03, "s3": -0.02, "s4": 0.02,
  "s5": 0.02, "s6": -0.001
}'