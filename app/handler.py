import logging

import pandas as pd
from core.dtypes import build_pydantic_model
from core.io import load_model, load_x_example, load_y_example
from pydantic import BaseModel as PydanticBaseModel

logger = logging.getLogger()


class ModelHandler:
    """Main class for handling inference model.

    NB!: The following variables need to be set in environment
    for proper class instantiation:

    - MODEL_PATH (path to cloudpickle-saved model)
    - MODEL_X_EXAMPLE (path to json-saved pandas DataFrame)
    - MODEL_Y_EXAMPLE (path to json-saved pandas DataFrame)
    """

    def __init__(self):
        logger.info('Initilazing ModelHandler.')

        # Загружаем модель
        self._model = load_model()

        # Загружаем примеры входных/выходных данных модели
        self._x_example: pd.DataFrame = load_x_example()
        self._y_example: pd.DataFrame = load_y_example()

        # Проверяем, что загруженная модель корректно работает
        self._check_model()

        # Название столбца с предсказанием модели
        self.output_label = self._y_example.columns[0]

        # Генерируем pydantic классы для входных/выходных данных
        self.input_pydantic_model: PydanticBaseModel = (
            build_pydantic_model('InputData', self._x_example)
        )
        self.output_pydantic_model: PydanticBaseModel = (
            build_pydantic_model('OutputData', self._y_example)
        )

        # Генерируем примеры входных/выходных данных, параллельно
        # проверяем корректность работы созданных pydantic классов
        self._input_example: dict = (
            self.input_pydantic_model
            .model_validate(self._x_example.iloc[0].to_dict())
            .model_dump()
        )
        self._output_example: dict = (
            self.output_pydantic_model
            .model_validate(self._y_example.iloc[0].to_dict())
            .model_dump()
        )

        # Добавляем сгенерированные примеры в конфигурацию pydantic классов
        # для их отображения в документации
        self.input_pydantic_model.model_config = {
            'json_schema_extra': {'examples': [self._input_example]}
        }
        self.output_pydantic_model.model_config = {
            'json_schema_extra': {'examples': [self._output_example]}
        }

        logger.info('ModelHandler initialisation completed.')

    def _check_model(self):
        """Check if loaded model predicts correct values."""

        prediction = self._model.predict(self._x_example)
        expected = self._y_example.to_numpy().ravel()

        if (prediction == expected).all():
            logger.info('Model prediction check passed.')
            return

        logger.error(
            f'Model prediction check failed, predicted: {prediction}, '
            f'expected: {expected}. Terminating.'
        )
        raise RuntimeError('Model check failed.')

    def predict(self, input: PydanticBaseModel) -> PydanticBaseModel:
        """Get model inference for input data."""
        # Конвертируем входные данные из pydantic в pd.DataFrame
        input_df = pd.DataFrame(
            [input.model_dump()],
            columns=self._x_example.columns
        )
        # Резульат возвращаем в формате pydantic
        return self.output_pydantic_model.model_validate(
            {self.output_label: self._model.predict(input_df)[0]}
        )
