"""
Simulation Routes - API endpoints for simulation control.

This module provides FastAPI routes for starting, stopping, and monitoring
MQTT simulations.
"""

from fastapi import APIRouter, HTTPException, Query

from ..models import (
    SimulationConfig,
    SimulationStatus,
    SimulationData,
    APIResponse,
)
from ..services.mqtt_service import mqtt_service

router = APIRouter(prefix="/simulation", tags=["simulation"])


@router.post("/start", response_model=APIResponse)
async def start_simulation(config: SimulationConfig):
    """Start a new MQTT simulation with the given configuration."""
    try:
        success = mqtt_service.start_simulation(config)

        if success:
            return APIResponse(
                success=True,
                message=(
                    f"Simulation started successfully with profile: "
                    f"{config.profile.name}"
                ),
                data={
                    "profile": config.profile.name,
                    "topic": config.profile.topic or "auto-generated",
                    "interval": config.interval,
                },
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Failed to start simulation. Check MQTT connection "
                    "and configuration."
                ),
            )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error starting simulation: {str(e)}"
        )


@router.post("/stop", response_model=APIResponse)
async def stop_simulation():
    """Stop the currently running simulation."""
    try:
        success = mqtt_service.stop_simulation()

        if success:
            return APIResponse(
                success=True, message="Simulation stopped successfully"
            )
        else:
            return APIResponse(
                success=False, message="No simulation is currently running"
            )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error stopping simulation: {str(e)}"
        )


@router.get("/status", response_model=SimulationStatus)
async def get_simulation_status():
    """Get the current simulation status."""
    try:
        return mqtt_service.get_simulation_status()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting simulation status: {str(e)}",
        )


@router.get("/data", response_model=SimulationData)
async def get_simulation_data(
    limit: int = Query(
        default=50, ge=1, le=100, description="Number of messages to return"
    )
):
    """Get recent simulation data."""
    try:
        data = mqtt_service.get_simulation_data(limit=limit)
        return SimulationData(**data)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting simulation data: {str(e)}"
        )
