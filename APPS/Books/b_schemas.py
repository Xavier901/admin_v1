from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    # published_year: Optional[str] = None

class BookRead(BookCreate):
    id: str