from app.exceptions import base

class FileDoesntExistError(base.NotFoundException):
    pass