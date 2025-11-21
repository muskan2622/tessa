"""
Risk Scoring Model
Custom model for title risk assessment
"""
from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import logging
import os

logger = logging.getLogger(__name__)


class RiskScoringModel:
    """Risk scoring model for title insurance"""
    
    def __init__(self):
        """Initialize risk scoring model"""
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def prepare_features(
        self,
        search_data: Dict[str, Any]
    ) -> np.ndarray:
        """
        Prepare features from title search data
        
        Args:
            search_data: Title search data dictionary
            
        Returns:
            Feature array
        """
        features = []
        
        # Number of liens
        features.append(len(search_data.get("liens", [])))
        
        # Number of encumbrances
        features.append(len(search_data.get("encumbrances", [])))
        
        # Number of deeds
        features.append(len(search_data.get("deeds", [])))
        
        # Total lien amount
        total_lien_amount = sum(
            lien.get("amount", 0) for lien in search_data.get("liens", [])
        )
        features.append(total_lien_amount)
        
        # Years since last deed
        if search_data.get("deeds"):
            latest_deed_date = max(
                deed.get("recording_date") for deed in search_data.get("deeds", [])
            )
            # TODO: Calculate years difference
            features.append(0)  # Placeholder
        else:
            features.append(0)
        
        # Has judgments
        has_judgments = 1 if search_data.get("judgments") else 0
        features.append(has_judgments)
        
        # Property age (if available)
        features.append(search_data.get("property_age", 0))
        
        return np.array(features).reshape(1, -1)
    
    def train(
        self,
        X: List[Dict[str, Any]],
        y: List[float]
    ):
        """
        Train the risk scoring model
        
        Args:
            X: List of title search data dictionaries
            y: List of risk scores (0-100)
        """
        # Prepare features
        X_features = np.vstack([self.prepare_features(x) for x in X])
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X_features)
        
        # Train model
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        logger.info("Risk scoring model trained successfully")
    
    def predict(
        self,
        search_data: Dict[str, Any]
    ) -> float:
        """
        Predict risk score
        
        Args:
            search_data: Title search data dictionary
            
        Returns:
            Risk score (0-100)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        # Prepare features
        features = self.prepare_features(search_data)
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Predict
        score = self.model.predict(features_scaled)[0]
        
        # Ensure score is between 0 and 100
        score = max(0, min(100, score))
        
        return float(score)
    
    def save_model(self, file_path: str):
        """Save model to file"""
        model_data = {
            "model": self.model,
            "scaler": self.scaler
        }
        joblib.dump(model_data, file_path)
        logger.info(f"Model saved to {file_path}")
    
    def load_model(self, file_path: str):
        """Load model from file"""
        model_data = joblib.load(file_path)
        self.model = model_data["model"]
        self.scaler = model_data["scaler"]
        self.is_trained = True
        logger.info(f"Model loaded from {file_path}")

