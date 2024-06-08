import logging
import os
import sys

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from utils import InputData

from core.io import load_model

load_dotenv()

# Настраиваем логгер
logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter(
        '%(asctime)s : %(levelname)s : %(filename)s : %(message)s'
    )
)
logger.addHandler(handler)
logger.setLevel(os.getenv('APP_LOG_LEVEL'))  # type: ignore
logger.info('App module is being initialized.')


app = FastAPI()

# handler = 


@app.get('/')
def healthcheck():
    return {'status': 'Service is up :)'}


@app.post('/predict')
def predict(input: InputData):
    return '/predict hadler called.'


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=os.getenv('APP_HOST_DOCKER'),  # type: ignore
        port=int(os.getenv('APP_PORT_DOCKER'))  # type: ignore
    )