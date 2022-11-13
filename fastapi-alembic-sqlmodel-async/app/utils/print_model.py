from fastapi.encoders import jsonable_encoder
from typing import TypeVar
from sqlmodel import SQLModel

ModelType = TypeVar("ModelType", bound=SQLModel)


def print_model(text: str = "", model: ModelType = []):
    """
    It prints sqlmodel responses for complex relationship models.
    """
    return print(text, jsonable_encoder(model))
