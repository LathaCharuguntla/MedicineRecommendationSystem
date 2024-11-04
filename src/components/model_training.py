import sys
from src.logger import logging
from src.exception import CustomException
from pathlib import Path
from src.constants import *
from src.entity.config_entity import ModelTrainerConfig
from src.utilis.common import read_yaml, create_directories, load_csv_data, save_json
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder


class ModelTrainer:
    def __init__(self, config_path=CONFIG_FILE_PATH):
        self.yaml_content = read_yaml(config_path)
        self.root_dir = Path(__file__).resolve().parents[2]
        self.config = ModelTrainerConfig(
            model_dir=self.yaml_content['model_training']['model_dir'],
            train_data_path=self.yaml_content['model_training']['train_data_path'],
            model_name=self.yaml_content['model_training']['model_name'],
            disease_list_path=self.yaml_content['model_training']['disease_list_path'],
            encoder_path = self.yaml_content['model_training']['encoder_path']
        )

    def creating_directories(self):
        try:
            create_directories(self.root_dir/self.config.model_dir)
            logging.info(f'Successfully created directory {self.config.model_dir}')
            create_directories(self.root_dir/self.config.disease_list_path)
            logging.info(f'Successfully created directory {self.config.disease_list_path}')
        except Exception as e:
            raise CustomException(e,sys)
        
    def loading_data(self):
        """Importing the train data"""
        try:
          self.train_data = load_csv_data(Path(self.root_dir/self.config.train_data_path))
          logging.info('Loaded train data successfully')
          return self.train_data
        except Exception as e:
            logging.error(f'Error Occured: {e}')
            raise CustomException(e,sys)
        
    def encoder(self,y):
        """Encoding the y and saving the encoder in json file"""
        try:
            encoder = LabelEncoder()
            y_transformed = encoder.fit_transform(y)
            joblib.dump(encoder,Path(self.root_dir/self.config.encoder_path))
            logging.info(f'Dumped the joblib encoder at file : {self.config.encoder_path}')

            disease_dict = dict(zip(range(len(encoder.classes_)), encoder.classes_))
            save_json(Path(self.root_dir/self.config.disease_list_path/'disease.json'), disease_dict)
            logging.info('Saved the disease list successfully to json file')
            
            return y_transformed

        except Exception as e:
            logging.error(f'Error Occured: {e}')
            raise CustomException(e,sys)
        
    def model_trainer(self):
        """Training the data"""
        self.creating_directories()

        try: 
            train_data= self.loading_data()

            logging.info('Preparing the data for model training')
            X_train = train_data.drop('prognosis', axis=1)
            y_train = train_data['prognosis']

            y_processed = self.encoder(y_train)
            
            logging.info('Training the model')
            model = LogisticRegression(random_state=42)
            model.fit(X_train, y_processed)

            model_path = Path(self.root_dir/self.config.model_dir/self.config.model_name)
            joblib.dump(model, model_path)

            logging.info(f'Dumped model {model} successfully')
    
        except Exception as e:
            logging.error(f'Error occured: {e}')
            raise CustomException(e, sys)



if __name__=='__main__':
    obj = ModelTrainer()
    obj.model_trainer()

