"""This module defines custom exception classes for handling HTTP status codes."""
from http import HTTPStatus


class CustomException(Exception):
    """Base custom exception class with default error code and message."""

    code = HTTPStatus.BAD_GATEWAY
    error_code = HTTPStatus.BAD_GATEWAY
    message = HTTPStatus.BAD_GATEWAY.description

    def __init__(self: "CustomException", message=None) -> None:
        """
        Initialize the custom exception.

        Args:
            message (str): Optional custom error message.
        """
        if message:
            self.message = message


class BadRequestException(CustomException):
    """Custom exception class for HTTP 400 Bad Request."""

    code = HTTPStatus.BAD_REQUEST
    error_code = HTTPStatus.BAD_REQUEST
    message = HTTPStatus.BAD_REQUEST.description


class NotFoundException(CustomException):
    """Custom exception class for HTTP 404 Not Found."""

    code = HTTPStatus.NOT_FOUND
    error_code = HTTPStatus.NOT_FOUND
    message = HTTPStatus.NOT_FOUND.description


class ForbiddenException(CustomException):
    """Custom exception class for HTTP 403 Forbidden."""

    code = HTTPStatus.FORBIDDEN
    error_code = HTTPStatus.FORBIDDEN
    message = HTTPStatus.FORBIDDEN.description


class UnauthorizedException(CustomException):
    """Custom exception class for HTTP 401 Unauthorized."""

    code = HTTPStatus.UNAUTHORIZED
    error_code = HTTPStatus.UNAUTHORIZED
    message = HTTPStatus.UNAUTHORIZED.description


class UnprocessableEntity(CustomException):
    """Custom exception class for HTTP 422 Unprocessable Entity."""

    code = HTTPStatus.UNPROCESSABLE_ENTITY
    error_code = HTTPStatus.UNPROCESSABLE_ENTITY
    message = HTTPStatus.UNPROCESSABLE_ENTITY.description


class DuplicateValueException(CustomException):
    """Custom exception class for duplicate value or HTTP 422 Unprocessable Entity."""

    code = HTTPStatus.UNPROCESSABLE_ENTITY
    error_code = HTTPStatus.UNPROCESSABLE_ENTITY
    message = HTTPStatus.UNPROCESSABLE_ENTITY.description
