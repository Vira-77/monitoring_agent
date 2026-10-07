"""
This module defines API routes for handling Disk-related data.
"""
from typing import List
from fastapi import APIRouter, Request
from domain.schemas import (
    ExceptionResponseSchema,
    GetDiskResponseSchema,
)
from domain.services import DiskService

disk_router = APIRouter()

@disk_router.get(
    "/",
    response_model=int,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_root(request: Request) -> int:
    """
    Route to get the status of the root of the Disk API route.

    Args:
        request (Request): The incoming request.

    Returns:
        int: http status code 200.
    """
    return 200

@disk_router.get(
    "/usage",
    response_model=List[GetDiskResponseSchema],
    # response_model_exclude={"id"},
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_disk(request: Request) -> List[GetDiskResponseSchema]:
    """
    Route to get a list of Disk data.

    Args:
        request (Request): The incoming request.

    Returns:
        List[GetDiskResponseSchema]: A list of Disk data as per the response model.
    """
    return await DiskService().get_Disk(request.app.state.monitortask)

@disk_router.get(
    "/total",
    response_model=GetDiskResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_total_disk(request: Request) -> GetDiskResponseSchema:
    """
    Route to get the total disk metric for each disk.

    Args:
        request (Request): The incoming request.

    Returns:
        GetDiskResponseSchema: The total Disk metric as per the response model.
    """
    disk_data = await DiskService().get_Disk(request.app.state.monitortask)
    return next((metric for metric in disk_data if metric.metric == "total"), None)


@disk_router.get(
    "/free",
    response_model=GetDiskResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_free_disk(request: Request) -> GetDiskResponseSchema:
    """
    Route to get the free disk metric for each disk.

    Args:
        request (Request): The incoming request.

    Returns:
        GetDiskResponseSchema: The free Disk metric as per the response model.
    """
    disk_data = await DiskService().get_Disk(request.app.state.monitortask)
    return next((metric for metric in disk_data if metric.metric == "free"), None)


@disk_router.get(
    "/percent",
    response_model=GetDiskResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_percent_disk(request: Request) -> GetDiskResponseSchema:
    """
    Route to get the Disk usage percent metric for each disk.

    Args:
        request (Request): The incoming request.

    Returns:
        GetDiskResponseSchema: The Disk usage percent metric as per the response model.
    """
    disk_data = await DiskService().get_Disk(request.app.state.monitortask)
    return next((metric for metric in disk_data if metric.metric == "percent"), None)


@disk_router.get(
    "/used",
    response_model=GetDiskResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_used_disk(request: Request) -> GetDiskResponseSchema:
    """
    Route to get the used Disk metric for each disk.

    Args:
        request (Request): The incoming request.

    Returns:
        GetDiskResponseSchema: The used Disk metric as per the response model.
    """
    disk_data = await DiskService().get_Disk(request.app.state.monitortask)
    return next((metric for metric in disk_data if metric.metric == "used"), None)


