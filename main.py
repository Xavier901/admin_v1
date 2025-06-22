from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from fastapi import FastAPI
from starlette_admin.contrib.sqla import Admin, ModelView
from db import engine, Base

from ADMIN.admin import admin
from APPS.Books.r_book import book_router
from Users.routes import router

app = FastAPI()  

app.include_router(book_router)
#app.include_router(router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        


admin.mount_to(app)

@app.get("/")
def index():        
    return {"message": "Welcome to the FastAPI Admin!"}

