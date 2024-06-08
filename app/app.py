import logging
import os
import sys

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from model import ModelHandler

load_dotenv()

# Настраиваем логгер
logger = logging.getLogger()
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(
    logging.Formatter(
        '%(asctime)s : %(levelname)s : %(filename)s : %(message)s'
    )
)
logger.addHandler(log_handler)
logger.setLevel(os.getenv('APP_LOG_LEVEL'))  # type: ignore
logger.info('App module is being initialized.')


app = FastAPI()

ModelHandler()


@app.get('/')
def healthcheck():
    return {'status': 'Service is up :)'}


@app.post('/predict')
def predict():
    return '/predict hadler called.'


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=os.getenv('APP_HOST_DOCKER'),  # type: ignore
        port=int(os.getenv('APP_PORT_DOCKER'))  # type: ignore
    )
