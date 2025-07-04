"""
API Models - Pydantic models for the MQTT Simulator API.

This module defines the data models used by the FastAPI endpoints.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class QoSLevel(int, Enum):
    """MQTT Quality of Service levels."""

    AT_MOST_ONCE = 0
    AT_LEAST_ONCE = 1
    EXACTLY_ONCE = 2


class MQTTConfig(BaseModel):
    """MQTT broker configuration."""

    host: str = Field(default="localhost", description="MQTT broker host")
    port: int = Field(
        default=1883, ge=1, le=65535, description="MQTT broker port"
    )
    username: Optional[str] = Field(
        default=None, description="MQTT broker username"
    )
    password: Optional[str] = Field(
        default=None, description="MQTT broker password"
    )
    keepalive: int = Field(
        default=60, ge=1, description="Keepalive interval in seconds"
    )
    clean_session: bool = Field(
        default=True, description="Start with clean session"
    )
    qos: QoSLevel = Field(
        default=QoSLevel.AT_LEAST_ONCE, description="Quality of Service level"
    )
    retained: bool = Field(
        default=False, description="Retain message for new subscribers"
    )
    last_will_topic: Optional[str] = Field(
        default=None, description="Last will topic"
    )
    last_will_message: Optional[str] = Field(
        default=None, description="Last will message"
    )
    last_will_qos: QoSLevel = Field(
        default=QoSLevel.AT_MOST_ONCE, description="Last will QoS"
    )


class ProfileConfig(BaseModel):
    """Profile configuration for simulation."""

    name: str = Field(
        ..., description="Profile name (weather, agriculture, energy, etc.)"
    )
    parameters: Dict[str, Any] = Field(
        default_factory=dict, description="Profile-specific parameters"
    )
    topic: Optional[str] = Field(
        default=None, description="Custom MQTT topic (optional)"
    )


class SimulationConfig(BaseModel):
    """Complete simulation configuration."""

    mqtt: MQTTConfig = Field(..., description="MQTT broker configuration")
    profile: ProfileConfig = Field(..., description="Profile configuration")
    interval: int = Field(
        default=5, ge=1, le=3600, description="Publishing interval in seconds"
    )
    duration: Optional[int] = Field(
        default=None, ge=1, description="Simulation duration in seconds"
    )


class SimulationStatus(BaseModel):
    """Current simulation status."""

    is_running: bool = Field(
        ..., description="Whether simulation is currently running"
    )
    is_connected: bool = Field(
        ..., description="Whether connected to MQTT broker"
    )
    profile_name: Optional[str] = Field(
        default=None, description="Current profile name"
    )
    topic: Optional[str] = Field(
        default=None, description="Current MQTT topic"
    )
    interval: Optional[int] = Field(
        default=None, description="Current publishing interval"
    )
    messages_sent: int = Field(
        default=0, description="Number of messages sent"
    )
    start_time: Optional[str] = Field(
        default=None, description="Simulation start time (ISO format)"
    )
    last_message: Optional[Dict[str, Any]] = Field(
        default=None, description="Last published message"
    )


class ProfileInfo(BaseModel):
    """Information about a simulation profile."""

    name: str = Field(..., description="Profile name")
    description: str = Field(..., description="Profile description")
    parameters: Dict[str, Any] = Field(
        ..., description="Available parameters and their types"
    )
    example_topic: str = Field(..., description="Example MQTT topic")
    example_payload: Dict[str, Any] = Field(..., description="Example payload")


class ProfileList(BaseModel):
    """List of available profiles."""

    profiles: List[ProfileInfo] = Field(..., description="Available profiles")


class SimulationData(BaseModel):
    """Simulation data response."""

    messages: List[Dict[str, Any]] = Field(
        ..., description="Recent published messages"
    )
    total_count: int = Field(..., description="Total number of messages sent")


class APIResponse(BaseModel):
    """Generic API response wrapper."""

    success: bool = Field(
        ..., description="Whether the operation was successful"
    )
    message: str = Field(..., description="Response message")
    data: Optional[Dict[str, Any]] = Field(
        default=None, description="Response data"
    )


class ErrorResponse(BaseModel):
    """Error response model."""

    success: bool = Field(default=False, description="Always false for errors")
    error: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(
        default=None, description="Error details"
    )
