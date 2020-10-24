from fastapi import FastAPI

from .middleware import configure_db
from .endpoints import user

app = FastAPI()

configure_db(app)

app.include_router(user.router, prefix="/users")
