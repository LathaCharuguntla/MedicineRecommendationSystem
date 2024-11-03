import os
from src.logger import logging
from src.exception import CustomException
import yaml
from ensure import ensure_annotations
from pathlib import Path
import sys
import pandas as pd
import json




@ensure_annotations
def read_yaml(file_path:Path):
    """To read the yaml file"""
    try:
        with open(file_path) as file:
            content = yaml.safe_load(file)
            logging.info(f'Loaded yaml {file} successfully')
            return content

    except Exception as e:
        logging.error(f'Error occured {e}')
        raise CustomException(e,sys)


@ensure_annotations
def create_directories(file_path:Path):
    """Creating the directories"""
    try:
        os.makedirs(file_path, exist_ok=True)
        logging.info('Created file directory successfully')
    except Exception as e:
        logging.error(f'Error Occured: {e}')
        raise CustomException(e,sys)



@ensure_annotations
def load_csv_data(file_path:Path):
    """Loading the csv data"""
    try: 
        data = pd.read_csv(file_path)
        logging.info('Loaded data successfully')
        return data
    except Exception as e:
        logging.error(f'Error Occured: {e}')
        raise CustomException(e,sys)
    

@ensure_annotations
def save_json(path:Path, data:dict):
    """Saving the file in json format"""
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
    logging.info(f'Saved json.dump(data, f, indent=4)json data at {path}')

        





if __name__=="__main__":
    content = load_csv_data(Path('../../artifacts/data_ingestion/diets.csv'))
    print(content.head())