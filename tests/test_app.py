# tests/test_app.py
import pytest
import os
import httpx

# 从环境变量获取 API URL 和预期版本
# 这些变量将在 GitHub Actions (release.yml) 中设置
BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8001")  # 默认测试 v0.1
EXPECTED_VERSION = os.getenv("MODEL_VERSION", "v0.1")

# 符合 scikit-learn diabetes 数据集的示例负载
PAYLOAD = {
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


@pytest.mark.parametrize("url", [f"{BASE_URL}/health"])
def test_health_check(url):
    """测试 /health 端点"""
    try:
        with httpx.Client() as client:
            response = client.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        assert data["status"] == "ok"
        assert data["model_version"] == EXPECTED_VERSION
    except httpx.ConnectError as e:
        pytest.fail(f"无法连接到 {url}。服务是否正在运行? 错误: {e}")


@pytest.mark.parametrize("url", [f"{BASE_URL}/predict"])
def test_predict(url):
    """使用有效数据测试 /predict 端点"""
    try:
        with httpx.Client() as client:
            response = client.post(url, json=PAYLOAD, timeout=10)
        response.raise_for_status()
        data = response.json()
        assert "prediction" in data
        assert isinstance(data["prediction"], float)
    except httpx.ConnectError as e:
        pytest.fail(f"无法连接到 {url}。服务是否正在运行? 错误: {e}")


@pytest.mark.parametrize("url", [f"{BASE_URL}/predict"])
def test_predict_bad_input(url):
    """测试 /predict 的无效输入（应返回 422）"""
    bad_payload = PAYLOAD.copy()
    del bad_payload["age"]  # 'age' 字段缺失

    with httpx.Client() as client:
        response = client.post(url, json=bad_payload, timeout=10)
    assert response.status_code == 422
