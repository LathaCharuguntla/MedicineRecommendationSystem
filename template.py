import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

list_of_files = [
    "src/__init__.py",
    "src/components/__init__.py",
    "src/utilis/__init__.py",
    "src/utilis/common.py",
    "src/pipeline/__init__.py",
    "src/entity/__init__.py",
    "src/entity/config_entity.py",
    "src/constants/__init__.py",
    "src/logger.py",
    "src/exception.py",
    "notebook/trails.ipynb",
    "config.yaml",
    "main.py",
    "app.py",
    "requirements.txt",
    "setup.py",
    "templates/index.html"
]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir!="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating file directory : f{filedir}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        with open(filepath, "w")  as f:
            pass
        logging.info(f"Creating file : {filepath}")

    else:
        logging.info("File exists")
