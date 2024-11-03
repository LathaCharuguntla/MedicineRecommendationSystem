from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_training import ModelTrainer
from src.components.model_evaluation import ModelEvaluation
from src.logger import logging
from src.exception import CustomException
import sys


class Pipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            logging.info('====================Entered the pipeline==================')

            logging.info('-----------------------Entered the Data Ingestion step-----------------------')
            dataingestion = DataIngestion()
            dataingestion.data_ingestion()
            logging.info('-----------------------Completed the Data Ingestion step-----------------------')
            
            logging.info('-----------------------Entered the Data Transformation step-----------------------')
            datatransformation = DataTransformation()
            datatransformation.data_transformation()
            logging.info('-----------------------Completed the Data Transformation step-----------------------')

            logging.info('-----------------------Entered the Model Trainer step-----------------------')
            modeltrainer = ModelTrainer()
            modeltrainer.model_trainer()
            logging.info('-----------------------Completed the Model Trainer step-----------------------')

            logging.info('-----------------------Entered the Model Evaluation step-----------------------')
            modelevalutaion = ModelEvaluation()
            modelevalutaion.model_evaluation()
            logging.info('-----------------------Completed the Model Evaluation Step-----------------------')

            logging.info('====================Completed the pipeline==================')

        except Exception as e:
            logging.error(f'Error Occured: {e}')
            raise CustomException(e,sys)





if __name__=='__main__':
    obj = Pipeline()
    obj.main()