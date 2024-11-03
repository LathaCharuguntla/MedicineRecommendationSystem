import sys
import os
from src.logger import logging
from src.exception import CustomException
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.utilis.common import read_yaml, create_directories, load_csv_data
from src.entity.config_entity import DataTransformationConfig
from pathlib import Path
from sklearn.model_selection import train_test_split
from src.constants import *


class DataTransformation:
    def __init__(self, config_path=CONFIG_FILE_PATH):
        logging.info('Entered Data Transformation')
        #self.yaml_path = Path('../../config.yaml')
        #self.yaml_path = CONFIG_FILE_PATH
        self.yaml_content = read_yaml(config_path)
        self.root_dir = Path(__file__).resolve().parents[2]
        self.config = DataTransformationConfig(root_dir=self.yaml_content['data_transformation']['root_dir'])
        #print(self.root_dir)
        self.data_transformation_path = self.root_dir/self.config.root_dir

    def creating_directories(self):
        """Create directories for saving transformed data, if they do not exist."""
        try:
            create_directories(self.data_transformation_path)
            logging.info(f'Directory created successfully at {self.data_transformation_path}')
        except Exception as e:
            logging.error(f'Failed to create directory {self.data_transformation_path}: {e}')
            raise CustomException(e,sys)

    def data_transformation(self):
        """Splitting the training data and testing data"""
        self.creating_directories()

        try:
            data_path = self.root_dir/'artifacts/data_ingestion/training.csv'
            self.data = load_csv_data(Path(data_path))
            logging.info(f'Loaded training data successfully \n {self.data.head()}')

            train_data, test_data = train_test_split(self.data, test_size=0.2, random_state=42)

            #print(self.config.root_dir)

            train_data.to_csv(Path(self.data_transformation_path)/'train.csv', index=False)
            logging.info('Saved the training data')

            test_data.to_csv(Path(self.data_transformation_path)/'test.csv', index=False)
            logging.info('Saved the test data')

        except Exception as e:
            logging.error(f'Error Occured: {e}')
            raise CustomException(e,sys)
        

if __name__=='__main__':
    obj = DataTransformation()
    obj.data_transformation()

    




