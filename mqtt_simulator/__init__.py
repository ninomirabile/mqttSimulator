"""
MQTT Simulator - A Python library for simulating real-time data publishing via
MQTT.

This package provides a modular framework for simulating various types of IoT
data (weather, agriculture, energy, etc.) and publishing them to MQTT brokers.
"""

__version__ = "0.1.0"
__author__ = "MQTT Simulator Contributors"
__license__ = "MIT"

from .core import MQTTClient
from .profiles import get_available_profiles

__all__ = ["MQTTClient", "get_available_profiles"]
