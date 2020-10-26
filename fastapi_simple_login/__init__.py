from fastapi import FastAPI

from .middleware import configure_db
from .endpoints import user, auth, resource
from .db import bootstrap

app = FastAPI(title="FastAPI Simple Login")

configure_db(app)
bootstrap()

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(auth.router, tags=["auth"])
app.include_router(resource.router, prefix="/resource", tags=["generic"])
