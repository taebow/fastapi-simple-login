import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

log = logging.getLogger(__name__)


class ServerError(Exception):
    status_code = 500

    def __init__(self, cause=None, *args, **kwargs):
        if args:
            self.message = self.message.format(*args) # noqa
        if kwargs:
            self.message = self.message.format(**kwargs) # noqa
        super().__init__(self.message)


class MissingSessionError(ServerError):
    message = "No session found!"


class CRUDOperationError(ServerError):
    pass


class CreateError(CRUDOperationError):
    status_code = 400
    message = "Could not create {model} with params={params}"


class UpdateError(CRUDOperationError):
    status_code = 400
    message = "Could not update {model} with {field}{value} and params={data}"


class GetError(CRUDOperationError):
    status_code = 400
    message = "Could not get {model} with {field}={value}"


class DeleteError(CRUDOperationError):
    status_code = 400
    message = "Could not delete {model} with {field}={value}"


def configure_exc_handler(app):
    @app.exception_handler(ServerError)
    async def exception_handler(request: Request, exc: ServerError):
        status_code = exc.status_code
        message = exc.message
        cause = None

        # To add
        if isinstance(exc.__cause__, IntegrityError):
            status_code = 403
            cause = "Duplicate resource error"

        if cause:
            message = f"{message} : {cause}"

        return JSONResponse(status_code=status_code, content=message)
