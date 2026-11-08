import joblib
import pandas as pd
from flask import Flask, request, jsonify

superkart_api = Flask("SuperKart Sales Predictor")
model = joblib.load("superkart_model.joblib")

@superkart_api.get("/")
def home():
    return "Welcome to the SuperKart Sales Prediction API!"

@superkart_api.post("/v1/predict")
def predict_sales():
    data = request.get_json()
    df = pd.DataFrame([data])
    prediction = model.predict(df)[0]
    return jsonify({"Predicted_Sales": round(float(prediction), 2)})

@superkart_api.post("/v1/predictbatch")
def predict_sales_batch():
    file = request.files["file"]
    df = pd.read_csv(file)
    predictions = model.predict(df)
    results = {i: round(float(p), 2) for i, p in enumerate(predictions)}
    return jsonify(results)

if __name__ == "__main__":
    superkart_api.run(host="0.0.0.0", port=7860)
