# maio-mlops-groupk
Assignment3 in MAIO

# To-do List
* 中文注释改英文？
* 整理README.md（见作业要求），全部改为英文
* 完成CHANGELOG.md
* 测试gitHub release的docker镜像是否能够pull，本地能否运行，以及其他老师会测试的部分（见作业要求） （补充v0.2 image shows a justified improvement (metrics + short rationale).）见CHANGELOG.md, 其他测试OK， 确认两个版本RMSE是否搞混？理论上RMSE最小模型效果越好
* 测试github actions页面是否显示老师要求的内容（（见作业要求）

# 虚拟糖尿病诊所 - 分诊 ML 服务

该服务为糖尿病进展提供风险评分，以帮助虚拟诊所优先安排患者随访。


## 模型版本与性能

| 版本 | 模型 | 测试集 RMSE |
| :--- | :--- | :--- |
| **v0.2** | `RandomForestRegressor` | 59.8588 |
| **v0.1** | `LinearRegression` | 56.3295 |

详细信息请参阅 `CHANGELOG.md`。

## 运行服务 (Docker Compose)

服务通过 GitHub Actions 构建并发布到 GHCR。根据作业 Q&A，请使用 `docker-compose` 来运行服务。

1.  **拉取并运行服务:**
    此命令将从 GHCR 拉取 `v0.1` 和 `v0.2` 镜像，并在后台启动它们。
    ```bash
    docker-compose up -d
    ```

2.  **验证服务:**
    * **v0.1** 运行在 `http://localhost:8001`
    * **v0.2** 运行在 `http://localhost:8002`

    检查健康状况：
    ```bash
    curl http://localhost:8001/health
    # 响应: {"status":"ok", "model_version": "v0.1"}
    
    curl http://localhost:8002/health
    # 响应: {"status":"ok", "model_version": "v0.2"}
    ```

3.  **停止服务:**
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
```


# MLOps 作业完整执行清单

这是一个从零开始完成 MLOps 作业（虚拟糖尿病诊所）的完整分步指南。

---

## 阶段 0：项目设置（一次性）

1.  **创建仓库：** 在 GitHub 上创建一个**公共**仓库（例如 `diabetes-mlops`）。
2.  **本地克隆：** `git clone <your-repo-url>`
3.  **创建文件：** 在本地创建所有项目文件和目录结构（`src/app.py`, `src/train.py`, `models/.gitkeep`, `tests/test_app.py`, `Dockerfile`, `docker-compose.yml`, `README.md`, `requirements.txt`, `.github/workflows/ci.yml`, `.github/workflows/release.yml` 等）。
4.  **关键修改：** 打开 `docker-compose.yml` 和 `README.md`，将所有 `<ORG>/<REPO>` 占位符替换为你自己的 GitHub `用户名/仓库名`。
5.  **创建环境：**
    ```bash
    conda create -n mlops python=3.11
    conda activate mlops
    ```
6.  **安装依赖：** ```bash
    pip install -r requirements-dev.txt
    ```
7.  **首次提交：**
    ```bash
    git add .
    git commit -m "Initial project setup"
    git push origin main
    ```

---

## 阶段 1：Iteration 1 (v0.1) - 基线发布

1.  **本地训练 (v0.1)：**
    * 运行 `python src/train.py --version v0.1`。
    * 这会创建 `models/model-v0.1.joblib` 并打印 v0.1 的 RMSE (例如 `53.8869`)。

2.  **创建 `CHANGELOG.md`：**
    * 创建 `CHANGELOG.md` 文件。
    * 添加 `[v0.1]` 条目，填入日期和上一步得到的 RMSE。

3.  **提交 v0.1 产物：**
    ```bash
    git add models/model-v0.1.joblib CHANGELOG.md
    git commit -m "feat(v0.1): Add baseline model and changelog"
    git push origin main
    ```

4.  **（如果提示格式问题）格式化和 Lint 修复：**
    * 在本地运行 `pip install black`。
    * 运行 `black .` 自动格式化代码。
    * 运行 `flake8 .` 检查并修复所有剩余错误（例如删除 `train.py` 中未使用的 `pandas` 导入）。
    * 提交修复：
        ```bash
        git add .
        git commit -m "style: Fix linting and format code"
        git push origin main
        ```

5.  **验证 CI (v0.1)：**
    * 去 GitHub "Actions" 标签页。
    * 等待 `ci.yml` 工作流（由 `push` 触发）**成功通过** (Lint ✅, Docker Build Test ✅)。

6.  **发布 v0.1 (Tag)：**
    ```bash
    git tag v0.1
    git push origin v0.1
    ```

7.  **验证 Release (v0.1)：**
    * 去 GitHub "Actions" 标签页。
    * 等待 `release.yml` 工作流（由 `v0.1` 标签触发）**成功通过**。
    * 检查 GitHub 上的 "Packages" 和 "Releases" 标签，确认 `v0.1` 已发布。

---

## 阶段 2：Iteration 2 (v0.2) - 改进发布

1.  **本地训练 (v0.2)：**
    * 运行 `python src/train.py --version v0.2`。
    * 这会创建 `models/model-v0.2.joblib` 并打印 v0.2 的 RMSE (例如 `48.8687`)。

2.  **更新文档 (v0.2)：**
    * 打开 `CHANGELOG.md`。
    * 将 `[v0.2]` 部分的内容（包括性能对比表格）**添加**到文件的**最顶部**（在 `[v0.1]` 部分的上方）。

3.  **提交 v0.2 产物：**
    ```bash
    git add models/model-v0.2.joblib CHANGELOG.md
    git commit -m "feat(v0.2): Add RandomForest model and update changelog"
    git push origin main
    ```

4.  **验证 CI (v0.2)：**
    * 去 GitHub "Actions" 标签页。
    * 等待 `ci.yml` 工作流（由 `push` 触发）**成功通过** (Lint ✅, Docker Build Test ✅)。

5.  **发布 v0.2 (Tag)：**
    ```bash
    git tag v0.2
    git push origin v0.2
    ```

6.  **验证 Release (v0.2)：**
    * 去 GitHub "Actions" 标签页。
    * 等待 `release.yml` 工作流（由 `v0.2` 标签触发）**成功通过**。
    * 检查 "Packages" 和 "Releases"，确认 `v0.2` 也已发布。

---

## 阶段 3：最终本地验证（教授的视角）

1.  **拉取镜像：** ```bash
    docker-compose pull
    ```
2.  **启动服务：** ```bash
    docker-compose up -d
    ```
3.  **测试 v0.1：** ```bash
    curl http://localhost:8001/health
    ```
    *(应返回 `{"status":"ok", "model_version": "v0.1"})*
    测试返回：{"status":"ok","model_version":"v0.1"}  测试通过

4.  **测试 v0.2：** ```bash
    curl http://localhost:8002/health
    ```
    *(应返回 `{"status":"ok", "model_version": "v0.2"})*
    测试返回：{"status":"ok","model_version":"v0.1"} 测试通过

5.  **测试 v0.2 预测：**
    ```bash
    curl -X POST http://localhost:8002/predict -H "Content-Type: application/json" -d \
    '{"age": 0.02, "sex": -0.044, "bmi": 0.06, "bp": -0.03, "s1": -0.02, "s2": 0.03, "s3": -0.02, "s4": 0.02, "s5": 0.02, "s6": -0.001}'
    ```
    *(应返回 `{"prediction": 140.5...}` 这样的浮点数)*
    测试返回：{"prediction":234.38433726207228} 测试通过

7.  **清理：** ```bash
    docker-compose down
    ```
8.  **提交作业：** 将你的 GitHub 仓库 URL 放入 PDF 中并提交。
