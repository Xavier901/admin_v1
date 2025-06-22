from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .b_schemas import BookCreate, BookRead
from db import async_session_maker
from .b_models import Book
from typing import Optional, List
from sqlalchemy import select


# --- FastAPI Router & CRUD ---
book_router = APIRouter()

# Dependency
async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

@book_router.post("/books/", response_model=BookRead)
async def create_book(book: BookCreate, session: AsyncSession = Depends(get_session)):
    new_book = Book(**book.dict())
    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    return new_book

@book_router.get("/books/", response_model=List[BookRead])
async def get_books(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book))
    return result.scalars().all()

@book_router.get("/books/{book_id}", response_model=BookRead)
async def get_book_by_id(book_id: str, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@book_router.delete("/books/{book_id}")
async def delete_book(book_id: str, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    await session.delete(book)
    await session.commit()
    return {"message": "Book deleted"}



@book_router.put("/books/{book_id}", response_model=BookRead)
async def update_book(
    book_id: str,
    updated_data: BookCreate,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for field, value in updated_data.dict(exclude_unset=True).items():
        setattr(book, field, value)

    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book

