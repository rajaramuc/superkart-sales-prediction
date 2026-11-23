
# Import necessary libraries
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize Flask app with a name
superkart_api = Flask("SuperKart")

# Load the trained model (preprocessing + regressor pipeline)
model = joblib.load("superkart_model.joblib")

# The features the model expects, in a fixed order
FEATURES = [
    "Product_Weight", "Product_Sugar_Content", "Product_Allocated_Area", "Product_MRP",
    "Store_Size", "Store_Location_City_Type", "Store_Type", "Product_Id_char",
    "Store_Age_Years", "Product_Type_Category",
]


# Home route
@superkart_api.get("/")
def home():
    return "Welcome to the SuperKart Sales Prediction API"


# Online inference: predict the sales for a single product-store combination
@superkart_api.post("/v1/predict")
def predict_sales():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    missing = [f for f in FEATURES if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    input_data = pd.DataFrame([{f: data[f] for f in FEATURES}])
    prediction = float(model.predict(input_data)[0])
    return jsonify({"Sales": round(prediction, 2)})


# Batch inference: predict the sales for every row of an uploaded CSV file
@superkart_api.post("/v1/predictbatch")
def predict_sales_batch():
    if "file" not in request.files:
        return jsonify({"error": "Upload a CSV file using the 'file' key"}), 400

    input_data = pd.read_csv(request.files["file"])
    missing = [f for f in FEATURES if f not in input_data.columns]
    if missing:
        return jsonify({"error": f"Missing columns: {missing}"}), 400

    predictions = model.predict(input_data[FEATURES]).tolist()
    # Map every row index to its predicted sales
    return jsonify({str(i): round(float(p), 2) for i, p in enumerate(predictions)})


# Local run only - in the container the app is served by Gunicorn
if __name__ == "__main__":
    superkart_api.run(host="0.0.0.0", port=7860, debug=False)
