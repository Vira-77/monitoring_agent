"""
This module defines API default routes for a router.

These routes handle health checks and basic information requests.
"""
from fastapi import APIRouter, Response, Request
from domain.schemas import (
    ExceptionResponseSchema,
    BasicResponseSchema
)
import socket

default_router = APIRouter()


@default_router.get("/health")
async def health() -> Response:
    """
    Health check route to indicate the service is running properly.

    Returns:
        Response: A response with a 200 status code.
    """
    return Response(status_code=200)


@default_router.get("/")
async def home() -> Response:
    """
    Home route to return a simple "Hello World" message.

    Returns:
        Response: A response with a "Hello World" message and a 200 status code.
    """
    return BasicResponseSchema(metric="message", value="Hello World")


@default_router.get("/version")
def last_version(request: Request) -> BasicResponseSchema:
    """
    Route to get the application's version.

    Args:
        request (Request): The incoming request.

    Returns:
        Response: A response containing the application's version and a 200 status code.
    """
    return BasicResponseSchema(metric="version", value=request.app.state.version)

@default_router.get(
    "/hostname",
    response_model=BasicResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}}
)
def get_hostname(request: Request) -> BasicResponseSchema:
    """
    Route to get the server's hostname.

    Args:
        request (Request): The incoming request.

    Returns:
        Response: A response containing the server's hostname and a 200 status code.
    """
    return BasicResponseSchema(metric="hostname", value=socket.gethostname())
