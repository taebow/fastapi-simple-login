from fastapi import FastAPI

from .exception import configure_exc_handler
from .middleware import configure_db
from .endpoints import user, auth, resource
from .db import bootstrap

app = FastAPI(title="FastAPI Simple Login")

configure_exc_handler(app)
configure_db(app)
bootstrap()

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(auth.router, tags=["auth"])
app.include_router(resource.router, prefix="/resource", tags=["generic"])

