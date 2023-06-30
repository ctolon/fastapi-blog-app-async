from app.exceptions import base


class BadCredentialsError(base.UnauthorizedException):
    pass


class TokenExpirateError(base.UnauthorizedException):
    pass


class TokenInvalidError(base.UnauthorizedException):
    pass


class UnAuthorizedError(base.UnauthorizedException):
    pass