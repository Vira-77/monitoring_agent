"""
This module contains a FastAPI application with various routes and middleware.

It initializes the FastAPI app, sets up routers, event listeners, and exception handlers, and
creates a monitoring thread for fetching metrics.
"""
from typing import List, AsyncGenerator
from fastapi import FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api import router
from api.default.default import default_router
from core.exceptions import CustomException
from core.config import get_config
from monitor import MonitorTask
from contextlib import asynccontextmanager
import asyncio

def init_routers(fastapi: FastAPI) -> None:
    """
    Initialize API routers and include them in the FastAPI fastapi.

    Args:
        fastapi (FastAPI): The FastAPI application to add routers to.
    """
    # Add default route (version, healthcheck)
    fastapi.include_router(default_router)
    # Add domain routes
    fastapi.include_router(router)


def init_listeners(fastapi: FastAPI) -> None:
    """
    Initialize event listeners and exception handlers for the FastAPI fastapi.

    Args:
        fastapi (FastAPI): The FastAPI application to set up event listeners and handlers for.
    """
    # Exception handler
    @fastapi.exception_handler(CustomException)
    async def custom_exception_handler(_request: Request, exc: CustomException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )

    # Start monitoring thread
    @asynccontextmanager
    async def on_start_up(fastapi: FastAPI) -> AsyncGenerator:
        task = asyncio.create_task(fastapi.state.monitor_task.monitor())
        try:
            yield
        finally:
            print("Shutting down monitor task...")
            task.cancel()


def make_middleware() -> List[Middleware]:
    """
    Create and return a list of middleware components, including CORS middleware.

    Returns:
        List[Middleware]: List of FastAPI middleware components.
    """
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
    ]
    return middleware


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: The configured FastAPI application.
    """
    config = get_config()
    # Monitoring thread to fetch metrics
    monitortask = MonitorTask()
    # API
    fastapi = FastAPI(
        title=config.title,
        description=config.description,
        version=config.version,
        docs_url="/docs",
        redoc_url="/redoc",
        middleware=make_middleware(),
    )
    fastapi.state.monitortask = monitortask
    fastapi.state.version = config.version
    init_routers(fastapi)
    init_listeners(fastapi)
    return fastapi


app = create_app()
