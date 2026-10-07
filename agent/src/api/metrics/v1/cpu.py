"""
This module defines API routes for handling CPU-related data.
"""
import psutil
from typing import List
from fastapi import APIRouter, Request
from domain.schemas import (
    ExceptionResponseSchema,
    GetCpuResponseSchema,
    GetCpuCoreResponseSchema,
    GetAverageResponseSchema
)
from domain.services import CpuService
from cpuinfo import get_cpu_info

cpu_router = APIRouter()

@cpu_router.get(
    "/",
    response_model=int,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_root(request: Request) -> int:
    """
    Route to get the status of the root of the Cpu API route.

    Args:
        request (Request): The incoming request.

    Returns:
        int: http status code 200.
    """
    return 200

@cpu_router.get(
    "/name",
    response_model=GetAverageResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_cpu_name(request: Request) -> GetAverageResponseSchema:
    """
    Route to get the name of the CPU.

    Args:
        request (Request): The incoming request.

    Returns:
        str: name of the CPU.
    """
    return GetAverageResponseSchema(metric="name", average_value=get_cpu_info()["brand_raw"])

@cpu_router.get(
    "/frequency",
    response_model=List[GetCpuCoreResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_cpu_frequency(request: Request) -> List[GetCpuCoreResponseSchema]:
    """
    Route to get the CPU frequency.

    Args:
        request (Request): The incoming request.

    Returns:
        List[GetCpuCoreResponseSchema]: List of CPU frequencies for each core.
    """
    try:
        obj = []
        for i, freq in enumerate(psutil.cpu_freq(percpu=True)):
            obj.append(GetCpuCoreResponseSchema(metric="frequency", number=int(freq.current)))

        return obj

    except Exception as e:
        return {"detail": f"Error retrieving CPU frequency: {str(e)}"}

@cpu_router.get(
    "/usage",
    response_model=List[GetCpuResponseSchema],
    # response_model_exclude={"id"},
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_cpu(request: Request) -> List[GetCpuResponseSchema]:
    """
    Route to get a list of CPU data.

    Args:
        request (Request): The incoming request.

    Returns:
        List[GetCpuResponseSchema]: A list of CPU data as per the response model.
    """
    return await CpuService().get_cpu(request.app.state.monitortask)


@cpu_router.get(
    "/core",
    response_model=GetCpuCoreResponseSchema,
    # response_model_exclude={"id"},
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_core_number(request: Request) -> GetCpuCoreResponseSchema:
    """
    Route to get the number of CPU core.

    Args:
        request (Request): The incoming request.

    Returns:
        str: name of the metric
        int: number of cpu core.
    """
    return GetCpuCoreResponseSchema(metric="core", number=request.app.state.monitortask.num_cores)

@cpu_router.get(
    "/averageuse",
    response_model=List[GetAverageResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_average(request: Request) -> List[GetAverageResponseSchema]:
    """
    Fetch the average CPU usage across all cores.

    This method calculates the average CPU usage from the usage percentages
    in the monitoring task and formats it as a dictionary containing the metric name and value.

    Args:
        monitor_task (MonitorTask): The monitoring task containing CPU usage data.

    Returns:
        dict: A dictionary containing the metric name ("averageuse") and the calculated average usage value.
        """
    average_data = await CpuService().get_Average(request.app.state.monitortask)
    return [average_data]