# Maio-MLOps-GroupK

# How to Run

## **(Step 0:) Local Training (v0.1 and v0.2):**


1. Remember to create your environment first!
2. Ridge model was used in v0.2 by default in train.py.

```bash
pip install \-r requirements-dev.txt
python src/train.py --version v0.1
python src/train.py --version v0.2
```

## **Step 1: Pull the Images**
```bash
docker pull ghcr.io/zhugt2019/maio-mlops-groupk:v0.1  
docker pull ghcr.io/zhugt2019/maio-mlops-groupk:v0.2
```


## **Step 2: Run the Containers**

```bash
docker run \-d \-p 8001:8000 \-e MODEL\_VERSION="v0.1" \--name MAIO-GroupK-v0.1 ghcr.io/zhugt2019/maio-mlops-groupk:v0.1
docker run \-d \-p 8002:8000 \-e MODEL\_VERSION="v0.2" \--name MAIO-GroupK-v0.2 ghcr.io/zhugt2019/maio-mlops-groupk:v0.2
```

## **Step 3: Verify**
```bash
curl http://localhost:8001/health  
curl http://localhost:8002/health
curl -X POST http://localhost:8002/predict -H "Content-Type: application/json" -d "{\"age\": 0.02, \"sex\": -0.044, \"bmi\": 0.06, \"bp\": -0.03, \"s1\": -0.02, \"s2\": 0.03, \"s3\": -0.02, \"s4\": 0.02, \"s5\": 0.02, \"s6\": -0.001}"
```

## **Step 4: Stop and Clean Up**

```bash
docker stop MAIO-GroupK-v0.1 MAIO-GroupK-v0.2  
docker rm MAIO-GroupK-v0.1 MAIO-GroupK-v0.2
```

# Grading Related Checklist

* **Runs on PR/push, fails on lint/tests:** The .github/workflows/ci.yml workflow runs on every push and pull request. Its Lint job (flake8 .) will fail the build if code style is incorrect.  
* **Seeds set:** src/train.py uses a fixed SEED \= 2025.
* **Env pinned:** requirements.txt pins all dependency versions to guarantee a consistent environment.  
* **Metrics logged & saved:** See CHANGELOG.md, or Changelog below.
* **Clear instructions to reproduce locally:** see above.
* **Self-contained:** The COPY ./models /app/models/ command ensures the pre-trained .joblib files are included directly in the image. 
* **Reasonable size:** It uses the python:3.11-slim base image for a small footprint.
* **Correct port exposed:** The EXPOSE 8000 instruction is included.


# Changelog

## [v0.2] - 2025-10-20

### What Changed
* **Model:** We changed the model from `LinearRegression` (v0.1) to `Ridge` (v0.2).

### Reason for Change
For version 0.2, we first tried more complex models like `RandomForest` and `GradientBoosting` to get a much lower error score.

However, our tests (shown in the table below) proved that these advanced models had a big **overfitting** problem. This means they were great at predicting the data they were trained on, but failed badly with new data.

So, we switched to the `Ridge` model. It gave us a slightly better score than our v0.1 baseline and was still good at predicting new data.

### Performance Scores

**Final Model Comparison:**

| Version | Model | Test RMSE (Error Score) |
| :--- | :--- | :--- |
| **v0.2** | `Ridge (alpha=1.0)` | **56.3131** |
| **v0.1** | `LinearRegression` | **56.3295** |

* **Improvement:** The error score was lowered by 0.0164. This is a small but clear improvement.

**Full Log of v0.2 Experiments:**

| Model We Tested | Train RMSE | Test RMSE | Conclusion |
| :--- | :--- | :--- | :--- |
| `Linear (v0.1)` | 52.8428 | **56.3295** | **Our starting point (baseline)** |
| `RandomForest` | 21.1479 | 59.8588 | Failed: Big Overfitting Problem |
| `RF (max_depth=10)` | 22.4564 | 60.1090 | Failed: Still Overfitting |
| `GridSearchCV(RF)` | 34.0756 | 60.2260 | Failed: Big Overfitting Problem |
| `GradientBoosting` | 22.9452 | 62.8603 | Failed: Big Overfitting Problem |
| **`Ridge (alpha=1.0)`** | 52.9258 | **56.3131** | **Success: This is our v0.2 Model** |

---

## [v0.1] - 2025-10-19

### What Changed
* **First Version:**
* **Model:** A simple `LinearRegression` model.
* **Score:** The starting error score (Test RMSE) was **56.3295**.
