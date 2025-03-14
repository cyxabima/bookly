from typing import Any, Callable
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.requests import Request


class BooklyException(Exception):
    """
    This is base class for all bookly errors
    """

    pass


class InvalidToken(BooklyException):
    """User has provided invalid or expired token"""

    pass


class RevokedToken(BooklyException):
    """User has provided token which has been revoked"""

    pass


class AccessTokenRequired(BooklyException):
    """User has provided Refresh token when access token is needed"""

    pass


class RefreshTokenRequired(BooklyException):
    """User has provided access token when  Refresh token is needed"""

    pass


class UserAlreadyExits(BooklyException):
    """User has provided email which is already present in database"""

    pass


class InSufficientPermissions(BooklyException):
    """User does not have permission to access these resources"""

    pass


class UserNotFound(BooklyException):
    """
    User is not present in database
    """

    pass


class InvalidCredentials(BooklyException):
    """User has provided invalid email or password"""

    pass


class BookNotFound(BooklyException):
    """
    Book with the provided uuid does not exits
    """

    pass


class TagNotFound(BooklyException):
    """
    Tag with this name already exits
    """

    pass


class TagAlreadyExits(BooklyException):
    pass


def create_exception_handler(
    status_code: int, initial_details: Any
) -> Callable[[Request, Exception], JSONResponse]:
    """Higher order function which return a function to raise a response"""

    def exception_handler(req: Request, ex: Exception) -> JSONResponse:
        return JSONResponse(content=initial_details, status_code=status_code)

    return exception_handler


def register_all_error(app: FastAPI):

    # Register exception handlers
    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_details={
                "message": "User not found",
                "resolution": "Please sign up first",
                "error_code": "USER_NOT_FOUND",
            },
        ),
    )

    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_details={
                "message": "Invalid or expired token",
                "resolution": "Please re-authenticate",
                "error_code": "INVALID_TOKEN",
            },
        ),
    )

    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_details={
                "message": "Token has been revoked",
                "resolution": "Please generate a new token",
                "error_code": "REVOKED_TOKEN",
            },
        ),
    )

    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_details={
                "message": "Access token is required",
                "resolution": "Use an access token instead of a refresh token",
                "error_code": "ACCESS_TOKEN_REQUIRED",
            },
        ),
    )

    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_details={
                "message": "Refresh token is required",
                "resolution": "Use a refresh token instead of an access token",
                "error_code": "REFRESH_TOKEN_REQUIRED",
            },
        ),
    )

    app.add_exception_handler(
        UserAlreadyExits,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_details={
                "message": "User already exists",
                "resolution": "Try signing in instead",
                "error_code": "USER_ALREADY_EXISTS",
            },
        ),
    )

    app.add_exception_handler(
        InSufficientPermissions,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_details={
                "message": "Insufficient permissions",
                "resolution": "Ensure you have the required permissions",
                "error_code": "INSUFFICIENT_PERMISSIONS",
            },
        ),
    )

    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_details={
                "message": "Invalid email or password",
                "resolution": "Check your credentials and try again",
                "error_code": "INVALID_CREDENTIALS",
            },
        ),
    )

    app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_details={
                "message": "Book not found",
                "resolution": "Check the book UUID and try again",
                "error_code": "BOOK_NOT_FOUND",
            },
        ),
    )

    app.add_exception_handler(
        TagNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_details={
                "message": "Tag not found",
                "resolution": "Ensure the tag exists before using it",
                "error_code": "TAG_NOT_FOUND",
            },
        ),
    )

    app.add_exception_handler(
        TagAlreadyExits,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_details={
                "message": "Tag already exists",
                "resolution": "Try using a different tag name",
                "error_code": "TAG_ALREADY_EXISTS",
            },
        ),
    )

    # statically or hardcoded special type of error every where
    # it is better to log here
    # here if dont uses class or do use class but use decorated syntax then
    # we have to make error function again and again for every error
    @app.exception_handler(500)
    async def internal_server_error(request, exc):
        return JSONResponse(
            content={
                "message": "Oops! Something went Wrong",
                "error_code": "SERVER_ERROR",
            }
        )
