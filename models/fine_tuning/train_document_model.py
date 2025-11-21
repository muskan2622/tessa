"""
Fine-tune Document Understanding Model
Train custom model for document classification and extraction
"""
import os
import json
from typing import List, Dict, Any
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding
)
from datasets import Dataset
import torch
import logging

logger = logging.getLogger(__name__)


class DocumentModelTrainer:
    """Train fine-tuned model for document understanding"""
    
    def __init__(
        self,
        base_model: str = "bert-base-uncased",
        num_labels: int = 7  # Number of document types
    ):
        """
        Initialize document model trainer
        
        Args:
            base_model: Base model to fine-tune
            num_labels: Number of document classification labels
        """
        self.base_model = base_model
        self.num_labels = num_labels
        self.tokenizer = AutoTokenizer.from_pretrained(base_model)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            base_model,
            num_labels=num_labels
        )
    
    def prepare_dataset(
        self,
        training_data: List[Dict[str, Any]]
    ) -> Dataset:
        """
        Prepare training dataset
        
        Args:
            training_data: List of training examples with 'text' and 'label' keys
            
        Returns:
            HuggingFace Dataset
        """
        texts = [ex["text"] for ex in training_data]
        labels = [ex["label"] for ex in training_data]
        
        # Tokenize
        encodings = self.tokenizer(
            texts,
            truncation=True,
            padding=True,
            max_length=512
        )
        
        # Create dataset
        dataset = Dataset.from_dict({
            "input_ids": encodings["input_ids"],
            "attention_mask": encodings["attention_mask"],
            "labels": labels
        })
        
        return dataset
    
    def train(
        self,
        train_dataset: Dataset,
        eval_dataset: Dataset = None,
        output_dir: str = "./models/document_model",
        num_epochs: int = 3,
        batch_size: int = 16,
        learning_rate: float = 2e-5
    ):
        """
        Train the model
        
        Args:
            train_dataset: Training dataset
            eval_dataset: Evaluation dataset (optional)
            output_dir: Directory to save model
            num_epochs: Number of training epochs
            batch_size: Training batch size
            learning_rate: Learning rate
        """
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=num_epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            learning_rate=learning_rate,
            weight_decay=0.01,
            logging_dir=f"{output_dir}/logs",
            logging_steps=10,
            eval_strategy="epoch" if eval_dataset else "no",
            save_strategy="epoch",
            load_best_model_at_end=True if eval_dataset else False
        )
        
        data_collator = DataCollatorWithPadding(tokenizer=self.tokenizer)
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            data_collator=data_collator,
            tokenizer=self.tokenizer
        )
        
        trainer.train()
        trainer.save_model(output_dir)
        self.tokenizer.save_pretrained(output_dir)
        
        logger.info(f"Model saved to {output_dir}")
    
    def load_model(self, model_path: str):
        """Load a trained model"""
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)

