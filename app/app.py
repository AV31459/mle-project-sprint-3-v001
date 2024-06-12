import logging
import os
import sys

import requests
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram

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

# Инструментатор для prometheus
Instrumentator().instrument(app).expose(app)

# Метрика: гистограмма предскзаний модели
metric_prediction_values = Histogram(
    'app_prediction_values',
    'Histogram of prediction values',
    buckets=[i * 1.e6 for i in range(30)]
)

# Метрика: счетчик необработанных исключений
metric_prediction_exception_counter = Counter(
    'app_prediction_exception_counter',
    'Number of unhandled prediction exceptions'
)


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
        metric_prediction_values.observe(
            getattr(response, handler.output_label)
        )
        logger.info(
            'Predict handler called. Input data (validated): '
            f'{input.model_dump_json()}, generated prediction: '
            f'{response.model_dump_json()}'
        )
        return response
    except Exception as exc:
        metric_prediction_exception_counter.inc()
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
        host=os.getenv('HOST_EXTERNAL'),  # type: ignore
        port=int(os.getenv('APP_PORT_EXTERNAL'))  # type: ignore
    )
