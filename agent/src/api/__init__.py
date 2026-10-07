from fastapi import APIRouter
from api.metrics.v1.cpu import cpu_router as cpu_v1_router
from api.metrics.v1.ram import ram_router as ram_v1_router
from api.metrics.v1.disk import disk_router as disk_v1_router
from api.metrics.v1.logs import logs_router as logs_v1_router

# Create a new APIRouter instance to manage the routes
router = APIRouter()

# Include the CPU-related routes with a versioned prefix
router.include_router(cpu_v1_router, prefix="/metrics/v1/cpu")
# Include the RAM-related routes with a versioned prefix
router.include_router(ram_v1_router, prefix="/metrics/v1/ram")
# Include the Disk-related routes with a versioned prefix
router.include_router(disk_v1_router, prefix="/metrics/v1/disk")
# Include the Logs-related routes with a versioned prefix
router.include_router(logs_v1_router, prefix="/metrics/v1/logs")

__all__ = ["router"]
