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

@dataclass
class ModelTrainerConfig:
    model_dir: Path
    train_data_path: Path
    test_data_path: Path
    model_name: str


