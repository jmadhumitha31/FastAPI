from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    title: str
    author: str
    genre: Optional[str] = None
    status: Optional[str] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    status: Optional[str] = None


class BookOut(BookBase):
    id: int
    added_at: datetime

    model_config = ConfigDict(from_attributes=True)
