"""
MQTT Routes - API endpoints for MQTT connection management.

This module provides FastAPI routes for testing MQTT broker connections.
"""

from fastapi import APIRouter, HTTPException

from ..models import MQTTConfig, APIResponse
from ..services.mqtt_service import mqtt_service

router = APIRouter(prefix="/mqtt", tags=["mqtt"])


@router.post("/connect", response_model=APIResponse)
async def test_mqtt_connection(config: MQTTConfig):
    """Test MQTT connection to the specified broker."""
    try:
        success = mqtt_service.test_mqtt_connection(
            host=config.host,
            port=config.port,
            username=config.username,
            password=config.password,
        )

        if success:
            return APIResponse(
                success=True,
                message=(
                    f"Successfully connected to MQTT broker at "
                    f"{config.host}:{config.port}"
                ),
                data={
                    "host": config.host,
                    "port": config.port,
                    "connected": True,
                },
            )
        else:
            return APIResponse(
                success=False,
                message=(
                    f"Failed to connect to MQTT broker at "
                    f"{config.host}:{config.port}"
                ),
                data={
                    "host": config.host,
                    "port": config.port,
                    "connected": False,
                },
            )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error testing MQTT connection: {str(e)}"
        )


@router.get("/status", response_model=APIResponse)
async def get_mqtt_status():
    """Get the current MQTT connection status."""
    try:
        status = mqtt_service.get_simulation_status()

        return APIResponse(
            success=True,
            message="MQTT connection status retrieved",
            data={
                "is_connected": status.is_connected,
                "is_running": status.is_running,
                "profile_name": status.profile_name,
                "topic": status.topic,
            },
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting MQTT status: {str(e)}"
        )
