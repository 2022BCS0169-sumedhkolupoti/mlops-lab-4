from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os

# Define the input data model
class WineFeatures(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float

app = FastAPI(title="Wine Quality Prediction API")

# Global variable to hold the model
model = None

@app.on_event("startup")
def load_model():
    global model
    try:
        model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
        model = joblib.load(model_path)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        # In a real app we might want to crash if model fails to load, 
        # but for now we'll just log it.
        raise e

@app.post("/predict")
def predict(features: WineFeatures):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Create a DataFrame from the input features
    # Map snake_case to the actual column names used during training
    data = {
        "fixed acidity": [features.fixed_acidity],
        "volatile acidity": [features.volatile_acidity],
        "citric acid": [features.citric_acid],
        "residual sugar": [features.residual_sugar],
        "chlorides": [features.chlorides],
        "free sulfur dioxide": [features.free_sulfur_dioxide],
        "total sulfur dioxide": [features.total_sulfur_dioxide],
        "density": [features.density],
        "pH": [features.pH],
        "sulphates": [features.sulphates],
        "alcohol": [features.alcohol]
    }
    
    df = pd.DataFrame(data)
    
    try:
        prediction = model.predict(df)
        quality = prediction[0]
        
        # Return the response in the specified format
        return {
            "name": "Sumedh Kolupoti", 
            "roll_no": "2022BCS0169",
            "wine_quality": float(quality)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Wine Quality Prediction API is running"}
