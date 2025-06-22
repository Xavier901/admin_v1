from db import engine
from starlette_admin.contrib.sqla import Admin, ModelView

# from ..APPS.Books.b_models import Book
from APPS.Books.b_models import Book

# from main import app


admin = Admin(engine, title="Tutorials: Basic",route_name= "admin")


admin.add_view(ModelView(Book, icon="fa-regular fa-book"))






