import pandas as pd
import logging
from core.io import load_model, load_y_example, load_x_example

logger = logging.getLogger()


class ModelHandler:
    """Main class for handling inference model."""

    def __init__(self):
        logger.debug('Initilazing ModelHandler.')
        self.model = load_model()
        self.x_example: pd.DataFrame = load_x_example()
        self.y_example: pd.DataFrame = load_y_example()
        self.check_model()
        logger.info('ModelHandler initialisation completed.')

    def check_model(self):
        """Check if loaded model predicts correct values."""

        prediction = self.model.predict(self.x_example)
        expected = self.y_example.to_numpy().ravel()
        if (prediction == expected).all():
            return
        logger.error(
            f'Model prediction check failed, predicted: {prediction}, '
            f'expected: {expected}. Terminating...'
        )
        raise RuntimeError('Model check failed')
