"""
Base Profile - Abstract base class for all simulation profiles.

This module defines the interface that all simulation profiles must implement.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from datetime import datetime
import json
import random


class BaseProfile(ABC):
    """Abstract base class for all simulation profiles."""

    def __init__(self, **kwargs):
        """Initialize the profile with optional configuration."""
        self.config = kwargs

    @abstractmethod
    def generate_data(self) -> Dict[str, Any]:
        """Generate simulated data for this profile."""
        pass

    @abstractmethod
    def get_topic(self) -> str:
        """Get the MQTT topic for this profile."""
        pass

    def get_payload(self) -> str:
        """Get the JSON payload for MQTT publishing."""
        data = self.generate_data()
        return json.dumps(data, default=str)

    def add_timestamp(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add ISO timestamp to the data."""
        data["timestamp"] = datetime.utcnow().isoformat() + "Z"
        return data

    def add_randomness(self, value: float, variance: float = 0.1) -> float:
        """Add random variance to a value."""
        return value + random.uniform(-variance * value, variance * value)

    def get_interval(self) -> int:
        """Get the publishing interval in seconds."""
        return self.config.get("interval", 5)
