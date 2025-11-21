"""
Fine-tuning Configuration
Configuration for model fine-tuning
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class FineTuningConfig:
    """Configuration for fine-tuning"""
    base_model: str = "bert-base-uncased"
    num_labels: int = 7
    max_length: int = 512
    batch_size: int = 16
    learning_rate: float = 2e-5
    num_epochs: int = 3
    weight_decay: float = 0.01
    warmup_steps: int = 100
    output_dir: str = "./models/fine_tuned"
    logging_dir: str = "./logs/fine_tuning"
    save_steps: int = 500
    eval_steps: int = 500
    seed: int = 42

