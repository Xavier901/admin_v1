
from sqlalchemy import Column, Integer, String, Boolean
from db import Base      # ✅ absolute import
import uuid


class Book(Base):
    __tablename__ = "books"
    # id = Column(Integer, primary_key=True)
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, index=True)
    author = Column(String)
    description = Column(String, nullable=True)
    # published_year = Column(Integer, nullable=True)