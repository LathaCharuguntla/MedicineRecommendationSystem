import os
import logging


log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, "running_logs.log")

logging_format = '[%(asctime)s: %(levelname)s: %(module)s: %(message)s]'

logging.basicConfig(
    level=logging.INFO,
    format=logging_format,
    handlers=[
        logging.FileHandler(log_file_path)
    ]
)


if __name__=="__main__":
    logging.info('Logging started')