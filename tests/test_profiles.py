"""
Unit tests for MQTT Simulator profiles.

This module contains tests for all profile classes and their Pydantic models.
"""

import pytest
import json
from datetime import datetime
from mqtt_simulator.profiles import get_available_profiles, get_profile
from mqtt_simulator.profiles.weather import WeatherProfile, WeatherData
from mqtt_simulator.profiles.agriculture import AgricultureProfile, SoilMoistureData
from mqtt_simulator.profiles.energy import EnergyProfile, EnergyData


class TestWeatherProfile:
    """Test cases for WeatherProfile."""
    
    def test_weather_profile_initialization(self):
        """Test WeatherProfile initialization with default values."""
        profile = WeatherProfile()
        assert profile.city == "Milano"
        assert profile.base_temp == 20.0
        assert profile.base_humidity == 60.0
        assert profile.base_wind == 10.0
    
    def test_weather_profile_custom_config(self):
        """Test WeatherProfile initialization with custom configuration."""
        profile = WeatherProfile(city="Roma", base_temp=25.0)
        assert profile.city == "Roma"
        assert profile.base_temp == 25.0
    
    def test_weather_data_generation(self):
        """Test weather data generation."""
        profile = WeatherProfile()
        data = profile.generate_data()
        
        # Check required fields
        assert "city" in data
        assert "temperature" in data
        assert "humidity" in data
        assert "wind_speed" in data
        assert "description" in data
        assert "timestamp" in data
        
        # Check data types and ranges
        assert isinstance(data["city"], str)
        assert isinstance(data["temperature"], (int, float))
        assert isinstance(data["humidity"], (int, float))
        assert isinstance(data["wind_speed"], (int, float))
        assert isinstance(data["description"], str)
        assert isinstance(data["timestamp"], str)
        
        # Check value ranges
        assert -50 <= data["temperature"] <= 60
        assert 0 <= data["humidity"] <= 100
        assert 0 <= data["wind_speed"] <= 200
    
    def test_weather_topic_generation(self):
        """Test MQTT topic generation."""
        profile = WeatherProfile(city="New York")
        topic = profile.get_topic()
        assert topic == "weather/new_york"
        
        profile = WeatherProfile(city="San Francisco")
        topic = profile.get_topic()
        assert topic == "weather/san_francisco"
    
    def test_weather_payload_generation(self):
        """Test JSON payload generation."""
        profile = WeatherProfile()
        payload = profile.get_payload()
        
        # Verify it's valid JSON
        data = json.loads(payload)
        assert isinstance(data, dict)
        assert "city" in data
    
    def test_weather_data_validation(self):
        """Test Pydantic model validation."""
        profile = WeatherProfile()
        data = profile.generate_data()
        
        # Validate with Pydantic model
        weather_data = profile.validate_data(data)
        assert isinstance(weather_data, WeatherData)
        assert weather_data.city == data["city"]
        assert weather_data.temperature == data["temperature"]


class TestAgricultureProfile:
    """Test cases for AgricultureProfile."""
    
    def test_agriculture_profile_initialization(self):
        """Test AgricultureProfile initialization with default values."""
        profile = AgricultureProfile()
        assert profile.sensor_id == "soil-001"
        assert profile.base_moisture == 40.0
        assert profile.base_temp == 18.0
        assert profile.base_ph == 6.5
        assert profile.soil_type == "loam"
    
    def test_agriculture_profile_custom_config(self):
        """Test AgricultureProfile initialization with custom configuration."""
        profile = AgricultureProfile(
            sensor_id="soil-002",
            soil_type="sandy",
            base_moisture=30.0
        )
        assert profile.sensor_id == "soil-002"
        assert profile.soil_type == "sandy"
        assert profile.base_moisture == 30.0
    
    def test_agriculture_data_generation(self):
        """Test agriculture data generation."""
        profile = AgricultureProfile()
        data = profile.generate_data()
        
        # Check required fields
        assert "sensor_id" in data
        assert "moisture" in data
        assert "temperature" in data
        assert "ph_level" in data
        assert "timestamp" in data
        
        # Check data types and ranges
        assert isinstance(data["sensor_id"], str)
        assert isinstance(data["moisture"], (int, float))
        assert isinstance(data["temperature"], (int, float))
        assert isinstance(data["ph_level"], (int, float))
        assert isinstance(data["timestamp"], str)
        
        # Check value ranges
        assert 0 <= data["moisture"] <= 100
        assert -10 <= data["temperature"] <= 50
        assert 0 <= data["ph_level"] <= 14
    
    def test_agriculture_topic_generation(self):
        """Test MQTT topic generation."""
        profile = AgricultureProfile(sensor_id="soil-123")
        topic = profile.get_topic()
        assert topic == "agriculture/soil/soil-123"
    
    def test_agriculture_payload_generation(self):
        """Test JSON payload generation."""
        profile = AgricultureProfile()
        payload = profile.get_payload()
        
        # Verify it's valid JSON
        data = json.loads(payload)
        assert isinstance(data, dict)
        assert "sensor_id" in data
    
    def test_agriculture_data_validation(self):
        """Test Pydantic model validation."""
        profile = AgricultureProfile()
        data = profile.generate_data()
        
        # Validate with Pydantic model
        soil_data = profile.validate_data(data)
        assert isinstance(soil_data, SoilMoistureData)
        assert soil_data.sensor_id == data["sensor_id"]
        assert soil_data.moisture == data["moisture"]


class TestEnergyProfile:
    """Test cases for EnergyProfile."""
    
    def test_energy_profile_initialization(self):
        """Test EnergyProfile initialization with default values."""
        profile = EnergyProfile()
        assert profile.meter_id == "energy-01"
        assert profile.base_power == 3.5
        assert profile.base_voltage == 230.0
        assert profile.base_current == 15.0
        assert profile.base_frequency == 50.0
        assert profile.load_pattern == "residential"
    
    def test_energy_profile_custom_config(self):
        """Test EnergyProfile initialization with custom configuration."""
        profile = EnergyProfile(
            meter_id="energy-02",
            load_pattern="industrial",
            base_power=50.0
        )
        assert profile.meter_id == "energy-02"
        assert profile.load_pattern == "industrial"
        assert profile.base_power == 50.0
    
    def test_energy_data_generation(self):
        """Test energy data generation."""
        profile = EnergyProfile()
        data = profile.generate_data()
        
        # Check required fields
        assert "meter_id" in data
        assert "power_kw" in data
        assert "voltage_v" in data
        assert "current_a" in data
        assert "frequency_hz" in data
        assert "timestamp" in data
        
        # Check data types and ranges
        assert isinstance(data["meter_id"], str)
        assert isinstance(data["power_kw"], (int, float))
        assert isinstance(data["voltage_v"], (int, float))
        assert isinstance(data["current_a"], (int, float))
        assert isinstance(data["frequency_hz"], (int, float))
        assert isinstance(data["timestamp"], str)
        
        # Check value ranges
        assert 0 <= data["power_kw"] <= 100
        assert 200 <= data["voltage_v"] <= 250
        assert 0 <= data["current_a"] <= 50
        assert 49 <= data["frequency_hz"] <= 51
    
    def test_energy_topic_generation(self):
        """Test MQTT topic generation."""
        profile = EnergyProfile(meter_id="meter-456")
        topic = profile.get_topic()
        assert topic == "energy/meter/meter-456"
    
    def test_energy_payload_generation(self):
        """Test JSON payload generation."""
        profile = EnergyProfile()
        payload = profile.get_payload()
        
        # Verify it's valid JSON
        data = json.loads(payload)
        assert isinstance(data, dict)
        assert "meter_id" in data
    
    def test_energy_data_validation(self):
        """Test Pydantic model validation."""
        profile = EnergyProfile()
        data = profile.generate_data()
        
        # Validate with Pydantic model
        energy_data = profile.validate_data(data)
        assert isinstance(energy_data, EnergyData)
        assert energy_data.meter_id == data["meter_id"]
        assert energy_data.power_kw == data["power_kw"]


class TestProfileRegistry:
    """Test cases for profile registry functionality."""
    
    def test_get_available_profiles(self):
        """Test getting available profiles."""
        profiles = get_available_profiles()
        
        assert isinstance(profiles, dict)
        assert "weather" in profiles
        assert "agriculture" in profiles
        assert "energy" in profiles
        
        # Check that all profiles are classes
        for profile_class in profiles.values():
            assert hasattr(profile_class, 'generate_data')
            assert hasattr(profile_class, 'get_topic')
    
    def test_get_profile(self):
        """Test getting a specific profile."""
        weather_profile = get_profile("weather")
        assert weather_profile == WeatherProfile
        
        agriculture_profile = get_profile("agriculture")
        assert agriculture_profile == AgricultureProfile
        
        energy_profile = get_profile("energy")
        assert energy_profile == EnergyProfile
    
    def test_get_invalid_profile(self):
        """Test getting an invalid profile raises an error."""
        with pytest.raises(ValueError, match="Profile 'invalid' not found"):
            get_profile("invalid")


class TestBaseProfile:
    """Test cases for BaseProfile functionality."""
    
    def test_add_timestamp(self):
        """Test timestamp addition to data."""
        from mqtt_simulator.profiles.base import BaseProfile
        
        class TestProfile(BaseProfile):
            def generate_data(self):
                return {"test": "data"}
            
            def get_topic(self):
                return "test/topic"
        
        profile = TestProfile()
        data = {"test": "data"}
        data_with_timestamp = profile.add_timestamp(data)
        
        assert "timestamp" in data_with_timestamp
        assert data_with_timestamp["test"] == "data"
        
        # Check timestamp format
        timestamp = data_with_timestamp["timestamp"]
        assert timestamp.endswith("Z")
        assert "T" in timestamp
    
    def test_add_randomness(self):
        """Test randomness addition to values."""
        from mqtt_simulator.profiles.base import BaseProfile
        
        class TestProfile(BaseProfile):
            def generate_data(self):
                return {"test": "data"}
            
            def get_topic(self):
                return "test/topic"
        
        profile = TestProfile()
        base_value = 100.0
        
        # Test with default variance
        result = profile.add_randomness(base_value)
        assert isinstance(result, float)
        assert 90.0 <= result <= 110.0  # ±10% variance
        
        # Test with custom variance
        result = profile.add_randomness(base_value, 0.2)
        assert isinstance(result, float)
        assert 80.0 <= result <= 120.0  # ±20% variance
    
    def test_get_interval(self):
        """Test interval retrieval."""
        from mqtt_simulator.profiles.base import BaseProfile
        
        class TestProfile(BaseProfile):
            def generate_data(self):
                return {"test": "data"}
            
            def get_topic(self):
                return "test/topic"
        
        # Test default interval
        profile = TestProfile()
        assert profile.get_interval() == 5
        
        # Test custom interval
        profile = TestProfile(interval=10)
        assert profile.get_interval() == 10 