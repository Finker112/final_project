from fastapi import FastAPI
import joblib
import os

app = FastAPI(title="出租车行程时间预测API")

# 定位模型文件
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "prod_model.joblib")

# 加载模型
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"模型加载失败：{e}")


@app.get("/")
def root():
    return {"service": "出租车行程时间预测API", "status": "running", "docs": "/docs"}


@app.post("/predict")
def predict(trip_distance: float, hour: int = 12, weekday: int = 2):
    features = [[trip_distance, hour, weekday]]
    duration = model.predict(features)[0]
    return {
        "predicted_duration_seconds": round(float(duration), 2),
        "input": {"trip_distance": trip_distance, "hour": hour, "weekday": weekday}
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)