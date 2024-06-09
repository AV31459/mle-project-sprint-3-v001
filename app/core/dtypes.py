from datetime import datetime

import pandas as pd
from pandas.io.json import build_table_schema
from pydantic import BaseModel as PydanticBaseModel
from pydantic import create_model


class Message(PydanticBaseModel):
    """Simple pydantic model for message output."""
    message: str = 'Some message here'


def get_pydantic_supported_dtype(json_schema_type: str):
    """
    Converts a string description of object data type to pydantic-supported
    python native type class (i.e. 'number' -> <class 'float'>, 'string' ->
    <class 'str'>, etc).
    """
    mapping = {
        'integer': int,
        'boolean': bool,
        'number': float,
        'datetime': datetime,
        'string': str
    }
    if json_schema_type not in mapping:
        raise ValueError(
            f'Unsupported field type {json_schema_type} in table json schema.'
        )
    return mapping[json_schema_type]


def build_pydantic_model(
    model_name: str,
    pandas_df: pd.DataFrame
) -> PydanticBaseModel:
    """Builds pydantic model class corresponding to given pandas DataFrame."""

    return create_model(
        model_name,
        **{
            field['name']:
            (get_pydantic_supported_dtype(field['type']), ...)
            for field
            in build_table_schema(pandas_df, index=False)['fields']
        }
    )
