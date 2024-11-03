from src.pipeline.pipeline import Pipeline
from src.logger import logging
from src.exception import CustomException
import sys



try:
    logging.info('>>>>>>>>>>>>>>>> Started the Program <<<<<<<<<<<<<<<<<<<')
    pip = Pipeline()
    pip.main()
    logging.info('>>>>>>>>>>>>>>>> Ended the Program Successfully<<<<<<<<<<<<<<<<<<<')

except Exception as e:
    logging.error(f'Error Occured: {e}')
    raise CustomException(e,sys)
