from typing import List, TypeVar
from pydantic import BaseModel
from sqlmodel import SQLModel


SchemaType = TypeVar("SchemaType", bound=BaseModel)
ModelType = TypeVar("ModelType", bound=SQLModel)


def map_models_schema(schema: SchemaType, models: List[ModelType]):
    return list(map(lambda model: schema.from_orm(model), models))
