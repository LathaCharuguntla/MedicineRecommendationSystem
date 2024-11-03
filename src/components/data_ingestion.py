import sys
import os
from pathlib import Path
from src.utilis.common import read_yaml, create_directories
from src.entity.config_entity import DataIngestionConfig
from src.logger import logging
from src.exception import CustomException
import requests
import pandas as pd
from src.constants import *
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


class DataIngestion:
    def __init__(self, config_path=CONFIG_FILE_PATH):
        logging.info('Entered the Data Ingestion')
        self.yaml_content = read_yaml(config_path)
        logging.info('Loaded Successfully yaml file')
        root_dir = Path(__file__).resolve().parents[2]
        self.artifacts_root = root_dir/self.yaml_content['artifacts_root']
        self.root_dir = root_dir/self.yaml_content['data_ingestion']['root_dir']

        self.config = DataIngestionConfig(
            root_dir=self.root_dir,
            source_url=self.yaml_content['data_ingestion']['source_url']
        )

    def creating_directories(self):
        """Creates necessary directories for data ingestion."""
        try:
            create_directories(self.artifacts_root)
            logging.info(f'Created directory : {self.artifacts_root}')
            create_directories(Path(self.config.root_dir))
            logging.info(f'Created directory: {self.config.root_dir}')
        except Exception as e:
            logging.error(f'Error Occured: {e}')
            raise CustomException(e,sys)

    def data_ingestion(self):
        """Ingests data from the configured URLs and saves it as CSV files."""
        self.creating_directories()
        self.url_lists = self.config.source_url
        self.file_name_list = ['training', 'description', 'diets', 'medications', 'precautions', 'symptoms', 'workout']

        try:
            for url,name in zip(self.url_lists, self.file_name_list):
                logging.info(f'Retrieving data from {url}')
                response = requests.get(url)
                json_data = response.json()
                data = pd.DataFrame(json_data)
                logging.info('Loaded data successfully from Url')

                path = self.root_dir/f'{name}.csv'
                data.to_csv(path, index=False)
                logging.info(f'Saved the {name} data successfully')

        except requests.exceptions.RequestException as e:
            logging.error(f'HTTP error occured : {e}')
            raise CustomException(e,sys)
        
        except Exception as e:
            logging.error(f'Error Occured: {e}')
            raise CustomException(e,sys)
       
    
if __name__=='__main__':
    obj = DataIngestion()
    content = obj.data_ingestion()