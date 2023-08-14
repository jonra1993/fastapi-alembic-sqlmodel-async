from typing import TypeVar
from pydantic import BaseModel
from sqlmodel import SQLModel


SchemaType = TypeVar("SchemaType", bound=BaseModel)
ModelType = TypeVar("ModelType", bound=SQLModel)


def map_models_schema(schema: SchemaType, models: list[ModelType]):
    return [schema.from_orm(model) for model in models]
