import logging
import os
# from datetime import datetime
import pandas as pd

import cloudpickle
from dotenv import load_dotenv
# from pandas.io.json import build_table_schema

load_dotenv()

logger = logging.getLogger()

model_path = os.path.abspath(os.getenv('MODEL_PATH'))
x_example_path = os.path.abspath(os.getenv('MODEL_X_EXAMPLE'))
y_example_path = os.path.abspath(os.getenv('MODEL_Y_EXAMPLE'))


def load_model():
    logger.debug(f'Loading model from: {model_path}')
    with open(model_path, 'rb') as fd:
        model = cloudpickle.load(fd)
    logger.info('Load model: OK.')
    return model


def load_x_example() -> pd.DataFrame:
    logger.debug(f'Loading x_example from: {x_example_path}')
    with open(x_example_path, 'rb') as fd:
        x_example = pd.read_json(fd, orient='table')
    logger.info('Load x_example: OK.')
    return x_example


def load_y_example() -> pd.DataFrame:
    logger.debug(f'Loading y_example from: {y_example_path}')
    with open(y_example_path, 'rb') as fd:
        y_example = pd.read_json(fd, orient='table')
    logger.info('Load y_example: OK.')
    return y_example
