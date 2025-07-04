"""
Energy Profile - Simulates energy meter data.

This module provides power consumption, voltage, current, and other
energy-related sensor data simulation.
"""

from typing import Dict, Any
from pydantic import BaseModel, Field
from .base import BaseProfile


class EnergyData(BaseModel):
    """Pydantic model for energy meter data."""

    meter_id: str = Field(..., description="Unique meter identifier")
    power_kw: float = Field(
        ..., ge=0, le=100, description="Power consumption in kW"
    )
    voltage_v: float = Field(
        ..., ge=200, le=250, description="Voltage in Volts"
    )
    current_a: float = Field(
        ..., ge=0, le=50, description="Current in Amperes"
    )
    frequency_hz: float = Field(
        ..., ge=49, le=51, description="Frequency in Hz"
    )
    timestamp: str = Field(..., description="ISO timestamp")


class EnergyProfile(BaseProfile):
    """Energy data simulation profile."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.meter_id = kwargs.get("meter_id", "energy-01")
        self.base_power = kwargs.get("base_power", 3.5)  # kW
        self.base_voltage = kwargs.get("base_voltage", 230.0)  # V
        self.base_current = kwargs.get("base_current", 15.0)  # A
        self.base_frequency = kwargs.get("base_frequency", 50.0)  # Hz

        # Simulate different load patterns
        self.load_pattern = kwargs.get("load_pattern", "residential")
        self.load_patterns = {
            "residential": {"min": 0.5, "max": 8.0, "variance": 0.3},
            "commercial": {"min": 2.0, "max": 25.0, "variance": 0.2},
            "industrial": {"min": 10.0, "max": 100.0, "variance": 0.1},
        }

    def generate_data(self) -> Dict[str, Any]:
        """Generate realistic energy meter data."""
        pattern = self.load_patterns.get(
            self.load_pattern, self.load_patterns["residential"]
        )

        # Generate power consumption based on load pattern
        power_variance = pattern["variance"]
        power = self.add_randomness(self.base_power, power_variance)
        power = max(pattern["min"], min(pattern["max"], power))

        # Generate voltage (relatively stable)
        voltage = self.add_randomness(self.base_voltage, 0.02)
        voltage = max(220, min(240, voltage))

        # Calculate current based on power and voltage
        current = (power * 1000) / voltage  # Convert kW to W, then calculate A
        current = self.add_randomness(current, 0.05)
        current = max(0, min(50, current))

        # Generate frequency (very stable)
        frequency = self.add_randomness(self.base_frequency, 0.01)
        frequency = max(49.8, min(50.2, frequency))

        data = {
            "meter_id": self.meter_id,
            "power_kw": round(power, 2),
            "voltage_v": round(voltage, 1),
            "current_a": round(current, 2),
            "frequency_hz": round(frequency, 2),
        }

        return self.add_timestamp(data)

    def get_topic(self) -> str:
        """Get the MQTT topic for energy data."""
        return f"energy/meter/{self.meter_id}"

    def validate_data(self, data: Dict[str, Any]) -> EnergyData:
        """Validate data using Pydantic model."""
        return EnergyData(**data)
