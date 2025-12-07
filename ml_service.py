import pandas as pd
import joblib
from xgboost import XGBClassifier
import os

# Paths to artifacts
MODEL_PATH = "xgb_lifestyle_model.json"
ENCODER_PATH = "label_encoder.pkl"
FEATURES_PATH = "feature_names.pkl"

class LifestylePredictor:
    def __init__(self):
        self.model = None
        self.label_encoder = None
        self.feature_names = None
        self.is_loaded = False
        
    def load_model(self):
        """Loads the model artifacts if they exist."""
        if not os.path.exists(MODEL_PATH) or \
           not os.path.exists(ENCODER_PATH) or \
           not os.path.exists(FEATURES_PATH):
            print("ML artifacts not found. Please run the training script first.")
            return False

        try:
            self.model = XGBClassifier()
            self.model.load_model(MODEL_PATH)
            
            self.label_encoder = joblib.load(ENCODER_PATH)
            self.feature_names = joblib.load(FEATURES_PATH)
            
            self.is_loaded = True
            print("Lifestyle model loaded successfully.")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False

    def predict(self, user_data: dict) -> str:
        """
        Predicts the lifestyle cluster for a user based on a dictionary of features.
        Returns 'Unknown' if model is not loaded or prediction fails.
        """
        if not self.is_loaded:
            if not self.load_model():
                return "Unknown"

        try:
            # Convert input dict to DataFrame
            df_input = pd.DataFrame([user_data])
            
            # One-Hot Encoding (if applicable, though usually we need to match training columns)
            # Since the model expects specific columns (including dummy variables like Gender_Male),
            # we need to ensure the input dataframe has EXACTLY those columns.
            
            # 1. Reindex to match training features (fills missing cols with 0)
            df_input = df_input.reindex(columns=self.feature_names, fill_value=0)
            
            # 2. Predict
            y_pred_encoded = self.model.predict(df_input)
            
            # 3. Decode label
            cluster_name = self.label_encoder.inverse_transform(y_pred_encoded)[0]
            
            return cluster_name
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return "Unknown"

# Singleton instance
predictor = LifestylePredictor()

def predict_user_cluster(user_data: dict) -> str:
    """Wrapper function to use easily in app.py"""
    return predictor.predict(user_data)

