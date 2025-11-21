"""
Document Labeling
Tools for creating labeled training datasets for document classification
"""
from typing import Dict, Any, List
from enum import Enum
import json


class DocumentLabel(str, Enum):
    """Document classification labels"""
    DEED = "deed"
    LIEN = "lien"
    MORTGAGE = "mortgage"
    TITLE_POLICY = "title_policy"
    SURVEY = "survey"
    ENCUMBRANCE = "encumbrance"
    JUDGMENT = "judgment"
    OTHER = "other"


class DocumentLabeler:
    """Label documents for training"""
    
    def __init__(self):
        self.labeled_data = []
    
    def label_document(
        self,
        document_id: str,
        document_type: DocumentLabel,
        extracted_fields: Dict[str, Any],
        confidence: float = 1.0
    ) -> Dict[str, Any]:
        """
        Label a document for training
        
        Args:
            document_id: Unique document identifier
            document_type: Document classification label
            extracted_fields: Extracted structured data
            confidence: Label confidence (0.0-1.0)
            
        Returns:
            Labeled document dictionary
        """
        labeled = {
            "document_id": document_id,
            "label": document_type.value,
            "extracted_fields": extracted_fields,
            "confidence": confidence,
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

