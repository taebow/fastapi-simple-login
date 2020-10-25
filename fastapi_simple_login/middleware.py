from starlette.middleware.base import (
    BaseHTTPMiddleware, RequestResponseEndpoint
)
from starlette.requests import Request
from starlette.types import ASGIApp

from .db import SessionManager


def configure_db(app):
    app.add_middleware(DBSessionMiddleware)


class DBSessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.session_manager = SessionManager()

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ):
        with self.session_manager:
            response = await call_next(request)
        return response
