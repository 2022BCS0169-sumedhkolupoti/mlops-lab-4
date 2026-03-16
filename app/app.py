from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os

app = Flask(__name__)

# Load model
model_path = 'model.pkl'
model = None
if os.path.exists(model_path):
    model = joblib.load(model_path)

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
    
    try:
        data = request.get_json()
        df = pd.DataFrame(data)
        prediction = model.predict(df)
        return jsonify({"prediction": prediction.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "model_loaded": model is not exists(model_path)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
