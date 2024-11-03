import sys
from src.logger import logging
from src.exception import CustomException
from pathlib import Path
from src.constants import *
from src.entity.config_entity import ModelTrainerConfig
from src.utilis.common import read_yaml, create_directories, load_csv_data
import joblib
from sklearn.linear_model import LogisticRegression


class ModelTrainer:
    def __init__(self, config_path=CONFIG_FILE_PATH):
        self.yaml_content = read_yaml(config_path)
        self.root_dir = Path(__file__).resolve().parents[2]
        self.config = ModelTrainerConfig(
            model_dir=self.yaml_content['model_training']['model_dir'],
            train_data_path=self.yaml_content['model_training']['train_data_path'],
            test_data_path=self.yaml_content['model_training']['test_data_path'],
            model_name=self.yaml_content['model_training']['model_name']
        )

    def creating_directories(self):
        try:
            create_directories(self.root_dir/self.config.model_dir)
            logging.info(f'Successfully created directory {self.config.model_dir}')
        except Exception as e:
            raise CustomException(e,sys)
        
    def loading_data(self):
        """Importing the train and test data"""
        try:
          self.train_data = load_csv_data(Path(self.root_dir/self.config.train_data_path))
          logging.info('Loaded train data successfully')
          self.test_data = load_csv_data(Path(self.root_dir/self.config.test_data_path))
          logging.info('Loaded test data successfully')
          return self.train_data, self.test_data
        except Exception as e:
            logging.error(f'Error Occured: {e}')
            raise CustomException(e,sys)
        
    def model_trainer(self):
        """Training the data"""
        self.creating_directories()

        try: 
            train_data, test_data = self.loading_data()

            logging.info('Preparing the data for model training')
            X_train = train_data.drop('prognosis', axis=1)
            y_train = train_data['prognosis']
            X_test = test_data.drop('prognosis', axis=1)
            y_test = test_data['prognosis']
            
            logging.info('Training the model')
            model = LogisticRegression(random_state=42)
            model.fit(X_train, y_train)

            model_path = Path(self.root_dir/self.config.model_dir/self.config.model_name)
            joblib.dump(model, model_path)

            logging.info(f'Dumped model {model} successfully')
    
        except Exception as e:
            logging.error(f'Error occured: {e}')
            raise CustomException(e, sys)



if __name__=='__main__':
    obj = ModelTrainer()
    obj.model_trainer()

