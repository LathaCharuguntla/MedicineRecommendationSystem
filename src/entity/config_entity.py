from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass
class DataIngestionConfig:
    root_dir:Path
    source_url: List[str]

@dataclass
class DataTransformationConfig:
    root_dir: Path
    symptoms_list_path: Path

@dataclass
class ModelTrainerConfig:
    model_dir: Path
    train_data_path: Path
    model_name: str
    disease_list_path: Path
    encoder_path: Path

@dataclass
class ModelEvaluationConfig:
    model_evaluation_path: Path
    model_path: Path
    test_data_path: Path
    metric_file_path: Path
    encoder_path: Path

