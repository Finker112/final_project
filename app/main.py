from fastapi import FastAPI
import mlflow.sklearn
import os

app = FastAPI(title="出租车行程时间预测API")

# 加载生产模型
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../ml/prod_model")
model = mlflow.sklearn.load_model(MODEL_PATH)

@app.post("/predict")
def predict(trip_distance: float, hour: int = 12, weekday: int = 2):
    """预测行程时长（秒）"""
    features = [[trip_distance, hour, weekday]]
    duration = model.predict(features)[0]
    return {
        "predicted_duration_seconds": round(float(duration), 2),
        "input": {"trip_distance": trip_distance, "hour": hour, "weekday": weekday}
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)