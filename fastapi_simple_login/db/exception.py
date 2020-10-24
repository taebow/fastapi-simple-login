import logging
from abc import ABC

log = logging.getLogger(__name__)


class ServerError(Exception, ABC):
    message: str

    def __init__(self, *args, **kwargs):
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
    message = "Could not create {model} with params : {params}"


class UpdateError(CRUDOperationError):
    message = "Could not update {instance}"


class GetError(CRUDOperationError):
    message = "Could not get {model} with id : {id}"


class DeleteError(CRUDOperationError):
    message = "Could not delete {instance}"
