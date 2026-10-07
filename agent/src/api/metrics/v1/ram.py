"""
This module defines API routes for handling RAM-related data.
"""
from fastapi import APIRouter, Request
from domain.schemas import (
    ExceptionResponseSchema,
    GetRamResponseSchema,
)
from domain.services import RamService

ram_router = APIRouter()


@ram_router.get(
    "/total",
    response_model=GetRamResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_total_ram(request: Request) -> GetRamResponseSchema:
    """
    Route to get the total RAM metric.

    Args:
        request (Request): The incoming request.

    Returns:
        GetRamResponseSchema: The total RAM metric as per the response model.
    """
    ram_data = await RamService().get_ram(request.app.state.monitortask)
    return next((metric for metric in ram_data if metric.metric == "total"), None)


@ram_router.get(
    "/free",
    response_model=GetRamResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_free_ram(request: Request) -> GetRamResponseSchema:
    """
    Route to get the free RAM metric.

    Args:
        request (Request): The incoming request.

    Returns:
        GetRamResponseSchema: The free RAM metric as per the response model.
    """
    ram_data = await RamService().get_ram(request.app.state.monitortask)
    return next((metric for metric in ram_data if metric.metric == "free"), None)


@ram_router.get(
    "/percent",
    response_model=GetRamResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_percent_ram(request: Request) -> GetRamResponseSchema:
    """
    Route to get the RAM usage percent metric.

    Args:
        request (Request): The incoming request.

    Returns:
        GetRamResponseSchema: The RAM usage percent metric as per the response model.
    """
    ram_data = await RamService().get_ram(request.app.state.monitortask)
    return next((metric for metric in ram_data if metric.metric == "percent"), None)


@ram_router.get(
    "/used",
    response_model=GetRamResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_used_ram(request: Request) -> GetRamResponseSchema:
    """
    Route to get the used RAM metric.

    Args:
        request (Request): The incoming request.

    Returns:
        GetRamResponseSchema: The used RAM metric as per the response model.
    """
    ram_data = await RamService().get_ram(request.app.state.monitortask)
    return next((metric for metric in ram_data if metric.metric == "used"), None)

