"""
MQTT Simulator Profiles - Plug-and-play data generators for different domains.

This module provides a registry of available simulation profiles and utilities
for discovering and loading them dynamically.
"""

from typing import Dict, Type
from .base import BaseProfile
from .weather import WeatherProfile
from .agriculture import AgricultureProfile
from .energy import EnergyProfile

# Registry of available profiles
_PROFILES: Dict[str, Type[BaseProfile]] = {
    "weather": WeatherProfile,
    "agriculture": AgricultureProfile,
    "energy": EnergyProfile,
}


def get_available_profiles() -> Dict[str, Type[BaseProfile]]:
    """Get all available simulation profiles."""
    return _PROFILES.copy()


def get_profile(profile_name: str) -> Type[BaseProfile]:
    """Get a specific profile by name."""
    if profile_name not in _PROFILES:
        raise ValueError(
            f"Profile '{profile_name}' not found. Available: "
            f"{list(_PROFILES.keys())}"
        )
    return _PROFILES[profile_name]


def register_profile(name: str, profile_class: Type[BaseProfile]) -> None:
    """Register a new profile."""
    _PROFILES[name] = profile_class


__all__ = [
    "BaseProfile",
    "WeatherProfile",
    "AgricultureProfile",
    "EnergyProfile",
    "get_available_profiles",
    "get_profile",
    "register_profile",
]
