"""
Agriculture Profile - Simulates agricultural sensor data.

This module provides soil moisture, temperature, and other agricultural
sensor data simulation.
"""

from typing import Dict, Any
from pydantic import BaseModel, Field
import random
from .base import BaseProfile


class SoilMoistureData(BaseModel):
    """Pydantic model for soil moisture data."""
    sensor_id: str = Field(..., description="Unique sensor identifier")
    moisture: float = Field(..., ge=0, le=100, description="Soil moisture percentage")
    temperature: float = Field(..., ge=-10, le=50, description="Soil temperature in Celsius")
    ph_level: float = Field(..., ge=0, le=14, description="Soil pH level")
    timestamp: str = Field(..., description="ISO timestamp")


class AgricultureProfile(BaseProfile):
    """Agriculture data simulation profile."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sensor_id = kwargs.get("sensor_id", "soil-001")
        self.base_moisture = kwargs.get("base_moisture", 40.0)
        self.base_temp = kwargs.get("base_temp", 18.0)
        self.base_ph = kwargs.get("base_ph", 6.5)
        
        # Different soil types have different moisture characteristics
        self.soil_type = kwargs.get("soil_type", "loam")
        self.moisture_variance = {
            "sandy": 0.4,  # Sandy soil dries quickly
            "clay": 0.1,   # Clay retains moisture
            "loam": 0.2,   # Loam is balanced
        }
    
    def generate_data(self) -> Dict[str, Any]:
        """Generate realistic agricultural sensor data."""
        # Generate soil moisture based on soil type
        moisture_variance = self.moisture_variance.get(self.soil_type, 0.2)
        moisture = self.add_randomness(self.base_moisture, moisture_variance)
        moisture = max(5, min(95, moisture))  # Keep within realistic bounds
        
        # Generate soil temperature (usually cooler than air temp)
        temp_variation = random.uniform(-3, 2)
        temperature = self.add_randomness(self.base_temp + temp_variation, 0.1)
        temperature = max(-5, min(35, temperature))
        
        # Generate pH level (slowly changing)
        ph_variation = random.uniform(-0.2, 0.2)
        ph_level = self.add_randomness(self.base_ph + ph_variation, 0.05)
        ph_level = max(5.0, min(8.5, ph_level))  # Most crops prefer 5.5-7.5
        
        data = {
            "sensor_id": self.sensor_id,
            "moisture": round(moisture, 1),
            "temperature": round(temperature, 1),
            "ph_level": round(ph_level, 1),
        }
        
        return self.add_timestamp(data)
    
    def get_topic(self) -> str:
        """Get the MQTT topic for agriculture data."""
        return f"agriculture/soil/{self.sensor_id}"
    
    def validate_data(self, data: Dict[str, Any]) -> SoilMoistureData:
        """Validate data using Pydantic model."""
        return SoilMoistureData(**data) 