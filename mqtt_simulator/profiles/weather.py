"""
Weather Profile - Simulates weather station data.

This module provides weather data simulation including temperature, humidity,
wind speed, and weather descriptions.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime
import random
from .base import BaseProfile


class WeatherData(BaseModel):
    """Pydantic model for weather data."""
    city: str = Field(..., description="City name")
    temperature: float = Field(..., ge=-50, le=60, description="Temperature in Celsius")
    humidity: float = Field(..., ge=0, le=100, description="Humidity percentage")
    wind_speed: float = Field(..., ge=0, le=200, description="Wind speed in km/h")
    description: str = Field(..., description="Weather description")
    timestamp: str = Field(..., description="ISO timestamp")


class WeatherProfile(BaseProfile):
    """Weather data simulation profile."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.city = kwargs.get("city", "Milano")
        self.base_temp = kwargs.get("base_temp", 20.0)
        self.base_humidity = kwargs.get("base_humidity", 60.0)
        self.base_wind = kwargs.get("base_wind", 10.0)
        
        # Weather descriptions for different conditions
        self.weather_descriptions = [
            "Clear Sky", "Partly Cloudy", "Cloudy", "Light Rain", 
            "Heavy Rain", "Thunderstorm", "Snow", "Fog", "Mist"
        ]
    
    def generate_data(self) -> Dict[str, Any]:
        """Generate realistic weather data."""
        # Generate temperature with seasonal variation
        temp_variation = random.uniform(-5, 5)
        temperature = self.add_randomness(self.base_temp + temp_variation, 0.15)
        
        # Generate humidity (inverse relationship with temperature)
        humidity = self.add_randomness(self.base_humidity, 0.2)
        if temperature > 25:
            humidity = max(30, humidity - 10)
        elif temperature < 10:
            humidity = min(90, humidity + 10)
        
        # Generate wind speed
        wind_speed = self.add_randomness(self.base_wind, 0.3)
        wind_speed = max(0, min(50, wind_speed))  # Cap at 50 km/h
        
        # Select weather description based on conditions
        if temperature < 0 and humidity > 70:
            description = "Snow"
        elif humidity > 80 and wind_speed > 20:
            description = "Thunderstorm"
        elif humidity > 70:
            description = random.choice(["Light Rain", "Heavy Rain", "Fog"])
        elif wind_speed > 30:
            description = "Clear Sky"  # Windy but clear
        else:
            description = random.choice(["Clear Sky", "Partly Cloudy", "Cloudy"])
        
        data = {
            "city": self.city,
            "temperature": round(temperature, 1),
            "humidity": round(humidity, 1),
            "wind_speed": round(wind_speed, 1),
            "description": description,
        }
        
        return self.add_timestamp(data)
    
    def get_topic(self) -> str:
        """Get the MQTT topic for weather data."""
        return f"weather/{self.city.lower().replace(' ', '_')}"
    
    def validate_data(self, data: Dict[str, Any]) -> WeatherData:
        """Validate data using Pydantic model."""
        return WeatherData(**data) 