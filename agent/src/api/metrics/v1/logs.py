import psutil
from typing import List
from fastapi import APIRouter, Request
from domain.schemas import (
    ExceptionResponseSchema,
    GetLogsResponseSchema,
    ProcessResourceUsageSchema,
    BasicResponseSchema,
    BasicIntResponseSchema,
    GetLogsLastErrorResponseSchema
)
from domain.services import LogsService
from monitor import MonitorTask

logs_router = APIRouter()

@logs_router.get(
    "/usage",
    response_model=List[GetLogsResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_logs(request: Request) -> List[GetLogsResponseSchema]:
    """
    Route to get a list of Logs data.

    Args:
        request (Request): The incoming request.

    Returns:
        List[GetLogsResponseSchema]: A list of Logs data as per the response model.
    """
    return await LogsService().get_logs(request.app.state.monitortask)

@logs_router.get(
    "/topprocesses",
    response_model=List[ProcessResourceUsageSchema],
    responses={"400": {"model": ExceptionResponseSchema}}
)
async def get_top_processes(request: Request) -> List[ProcessResourceUsageSchema]:
    """
    Route pour obtenir les processus qui utilisent le plus de ressources CPU et RAM.

    Args:
        request (Request): The incoming request.

    Returns:
        List[ProcessResourceUsageSchema]: List of top processes.
    """
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                process = proc.info

                if process['cpu_percent'] is not None and process['memory_info'] is not None:
                    processes.append({
                        'name': process['name'],
                        'cpu_consumption': process['cpu_percent'],
                        'ram_consumption': process['memory_info'].rss / (1024 * 1024)  # en Mo
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        processes = sorted(processes, key=lambda x: (x['cpu_consumption'], x['ram_consumption']), reverse=True)

        return processes[:5]

    except Exception as e:
        return {"detail": f"Error retrieving top processes: {str(e)}"}

@logs_router.get(
    "/error_count",
    response_model=BasicIntResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_error_count(request: Request) -> BasicIntResponseSchema:
    """
    Route to get the total number of errors that occurred (status code >= 400).

    Args:
        request (Request): The incoming request.

    Returns:
        BasicIntResponseSchema: A response model containing the error count.
    """
    monitor_task: MonitorTask = request.app.state.monitortask
    error_count = monitor_task.wordpress_error_count
    return BasicIntResponseSchema(metric="error_count", value=error_count)

@logs_router.get(
    "/last_errors",
    response_model=List[GetLogsLastErrorResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_last_errors(request: Request) -> List[GetLogsLastErrorResponseSchema]:
    """
    Route to get the last 5 error logs (status code >= 400).

    Args:
        request (Request): The incoming request.

    Returns:
        List[GetLogsResponseSchema]: A list of error logs.
    """
    monitor_task: MonitorTask = request.app.state.monitortask
    error_logs = monitor_task.wordpress_error_logs

    return [
        GetLogsLastErrorResponseSchema(
            status=log['status'],
            message=log['message'],
            error=log['error'],
            timestamp=log['timestamp'],
            level=log['level'],
            logger=log['logger'],
            method=log['method'],
            path=log['path']
        ) for log in error_logs
    ]

@logs_router.get(
    "/most_viewed_page",
    response_model=BasicResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_most_viewed_page(request: Request) -> BasicResponseSchema:
    """
    Route to get the most viewed page from the logs.

    Args:
        request (Request): The incoming request.

    Returns:
        BasicResponseSchema: A response model containing the most viewed page.
    """
    monitor_task: MonitorTask = request.app.state.monitortask
    counter = {}

    paths = [log['path'] for log in monitor_task.wordpress_logs]
    
    for path in paths:
        counter[path] = 0

    for path in paths:
        counter[path] += 1
    
    most_viewed_page = max(counter, key=counter.get)

    return BasicResponseSchema(
        metric="most_viewed_page",
        value="Most viewed page " + most_viewed_page + " with " + str(counter[most_viewed_page]) + " views"
    )