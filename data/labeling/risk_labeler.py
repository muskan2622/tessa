"""
Risk Labeling
Tools for creating labeled training datasets for risk scoring
"""
from typing import Dict, Any, List
from enum import Enum
import json


class RiskLabel(str, Enum):
    """Risk classification labels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskLabeler:
    """Label risk scores for training"""
    
    def __init__(self):
        self.labeled_data = []
    
    def label_risk(
        self,
        search_id: str,
        risk_score: float,
        risk_level: RiskLabel,
        risk_factors: List[Dict[str, Any]],
        actual_outcome: str = None  # "claim", "no_claim", etc.
    ) -> Dict[str, Any]:
        """
        Label a risk assessment for training
        
        Args:
            search_id: Title search identifier
            risk_score: Numeric risk score (0-100)
            risk_level: Risk level label
            risk_factors: List of risk factors
            actual_outcome: Actual outcome (for supervised learning)
            
        Returns:
            Labeled risk dictionary
        """
        labeled = {
            "search_id": search_id,
            "risk_score": risk_score,
            "risk_level": risk_level.value,
            "risk_factors": risk_factors,
            "actual_outcome": actual_outcome,
            "created_at": None  # Will be set by system
        }
        
        self.labeled_data.append(labeled)
        return labeled
    
    def export_labeled_data(self, file_path: str):
        """Export labeled data to JSON file"""
        with open(file_path, "w") as f:
            json.dump(self.labeled_data, f, indent=2, default=str)
    
    def load_labeled_data(self, file_path: str):
        """Load labeled data from JSON file"""
        with open(file_path, "r") as f:
            self.labeled_data = json.load(f)

