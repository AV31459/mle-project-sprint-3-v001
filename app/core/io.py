import logging
import os
import pandas as pd

import cloudpickle
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger()


def load_model():
    """Load cloudpickle-saved model from MODEL_PATH in environment."""
    model_path = os.path.abspath(os.getenv('MODEL_PATH'))
    logger.debug(f'Loading model from: {model_path}')

    with open(model_path, 'rb') as fd:
        model = cloudpickle.load(fd)

    logger.info('Load model: OK.')
    return model


def load_x_example() -> pd.DataFrame:
    """Load model input example (saved in json as pandas dataframe)
    from MODEL_X_EXAMPLE in environment.
    """

    x_example_path = os.path.abspath(os.getenv('MODEL_X_EXAMPLE'))
    logger.debug(f'Loading x_example from: {x_example_path}')

    with open(x_example_path, 'rb') as fd:
        x_example = pd.read_json(fd, orient='table')

    logger.info('Load x_example: OK.')
    return x_example


def load_y_example() -> pd.DataFrame:
    """Load model output example (saved in json as pandas dataframe)
    from MODEL_Y_EXAMPLE in environment.
    """

    y_example_path = os.path.abspath(os.getenv('MODEL_Y_EXAMPLE'))
    logger.debug(f'Loading y_example from: {y_example_path}')

    with open(y_example_path, 'rb') as fd:
        y_example = pd.read_json(fd, orient='table')

    logger.info('Load y_example: OK.')
    return y_example
