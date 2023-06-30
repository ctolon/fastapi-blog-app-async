from app.exceptions import base

class DbConnectionError(base.InternalServerException):
    pass