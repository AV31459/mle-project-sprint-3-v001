import logging
import os
import sys

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import requests

from core.dtypes import Message
from handler import ModelHandler

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

# Инициализируем объект-хендлер для модели
handler = ModelHandler()

# Основной объект приложения
app = FastAPI()


# Healthcheck uri
@app.get('/healthcheck', response_model=Message)
def healthcheck():
    return Message(message='Service seems to be up :)')


# Основной uri для получения предсказаний модели
@app.post('/predict', response_model=handler.output_pydantic_model)
def predict(
    # Используем динамически сгенерированный pydantic класс для валидации
    # входного json с помощью стандартной магии FasAPI
    input: handler.input_pydantic_model  # type: ignore
):
    try:
        response = handler.predict(input)
        logger.info(
            'Predict handler called. Input data (validated): '
            f'{input.model_dump_json()}, generated prediction: '
            f'{response.model_dump_json()}'
        )
        return response
    except Exception as exc:
        logger.error(
            'While predicting for input data (validated): \n'
            f'{input.model_dump_json(indent=4)} \n '
            f'the following exception was raised: \n {exc} \n',
            exc_info=True
        )
        raise HTTPException(
            status_code=requests.codes['/o\\'],
            detail='Internal server error'
        )


logger.info('App module initialization completed.')

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=os.getenv('APP_HOST_DOCKER'),  # type: ignore
        port=int(os.getenv('APP_PORT_DOCKER'))  # type: ignore
    )
