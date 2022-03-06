from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class SongBase(SQLModel):
    name: str
    artist: str
    year: Optional[int] = None


class Song(SongBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)
    updated_at: Optional[datetime]
    created_at: Optional[datetime]
