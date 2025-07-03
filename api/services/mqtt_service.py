"""
MQTT Service - Business logic for MQTT simulation management.

This module provides the service layer for managing MQTT simulations
through the API, including starting, stopping, and monitoring simulations.
"""

import asyncio
import json
import logging
import threading
import time
from datetime import datetime
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field

from mqtt_simulator import MQTTClient
from mqtt_simulator.profiles import get_available_profiles, get_profile
from ..models import SimulationConfig, SimulationStatus, ProfileInfo


@dataclass
class SimulationState:
    """Internal simulation state."""
    is_running: bool = False
    is_connected: bool = False
    client: Optional[MQTTClient] = None
    config: Optional[SimulationConfig] = None
    start_time: Optional[datetime] = None
    messages_sent: int = 0
    last_message: Optional[Dict[str, Any]] = None
    thread: Optional[threading.Thread] = None
    stop_event: threading.Event = field(default_factory=threading.Event)


class MQTTService:
    """Service for managing MQTT simulations."""
    
    def __init__(self):
        """Initialize the MQTT service."""
        self.simulation_state = SimulationState()
        self.logger = logging.getLogger(__name__)
        self._message_history: List[Dict[str, Any]] = []
        self._max_history = 100  # Keep last 100 messages
    
    def get_available_profiles(self) -> List[ProfileInfo]:
        """Get information about all available profiles."""
        profiles = get_available_profiles()
        profile_infos = []
        
        for name, profile_class in profiles.items():
            try:
                # Create an instance to get example data
                instance = profile_class()
                example_data = instance.generate_data()
                example_topic = instance.get_topic()
                
                # Get parameter information from the profile
                parameters = {}
                if hasattr(instance, 'config'):
                    parameters = instance.config.copy()
                
                profile_info = ProfileInfo(
                    name=name,
                    description=profile_class.__doc__ or f"{name.title()} data simulation profile",
                    parameters=parameters,
                    example_topic=example_topic,
                    example_payload=example_data
                )
                profile_infos.append(profile_info)
                
            except Exception as e:
                self.logger.warning(f"Error getting info for profile {name}: {e}")
                # Add basic info even if there's an error
                profile_info = ProfileInfo(
                    name=name,
                    description=f"{name.title()} data simulation profile",
                    parameters={},
                    example_topic=f"{name}/example",
                    example_payload={"error": "Could not generate example"}
                )
                profile_infos.append(profile_info)
        
        return profile_infos
    
    def get_profile_info(self, profile_name: str) -> Optional[ProfileInfo]:
        """Get information about a specific profile."""
        try:
            profile_class = get_profile(profile_name)
            instance = profile_class()
            example_data = instance.generate_data()
            example_topic = instance.get_topic()
            
            parameters = {}
            if hasattr(instance, 'config'):
                parameters = instance.config.copy()
            
            return ProfileInfo(
                name=profile_name,
                description=profile_class.__doc__ or f"{profile_name.title()} data simulation profile",
                parameters=parameters,
                example_topic=example_topic,
                example_payload=example_data
            )
        except Exception as e:
            self.logger.error(f"Error getting profile info for {profile_name}: {e}")
            return None
    
    def generate_profile_preview(self, profile_name: str, parameters: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate a preview of data for a profile with given parameters."""
        try:
            profile_class = get_profile(profile_name)
            instance = profile_class(**parameters)
            return instance.generate_data()
        except Exception as e:
            self.logger.error(f"Error generating preview for {profile_name}: {e}")
            return None
    
    def start_simulation(self, config: SimulationConfig) -> bool:
        """Start a new simulation with the given configuration."""
        if self.simulation_state.is_running:
            self.logger.warning("Simulation is already running")
            return False
        
        try:
            # Create MQTT client
            client = MQTTClient(
                broker_host=config.mqtt.host,
                broker_port=config.mqtt.port,
                username=config.mqtt.username,
                password=config.mqtt.password,
                keepalive=config.mqtt.keepalive,
                interval=config.interval
            )
            
            # Set up profile
            profile_class = get_profile(config.profile.name)
            profile_instance = profile_class(**config.profile.parameters)
            
            # Override topic if specified
            if config.profile.topic:
                # Monkey patch the get_topic method
                profile_instance.get_topic = lambda: config.profile.topic
            
            # Connect to broker
            if not client.connect():
                self.logger.error("Failed to connect to MQTT broker")
                return False
            
            # Set up the profile
            client.profile = profile_instance
            
            # Update state
            self.simulation_state.client = client
            self.simulation_state.config = config
            self.simulation_state.is_connected = client.is_connected
            self.simulation_state.is_running = True
            self.simulation_state.start_time = datetime.utcnow()
            self.simulation_state.messages_sent = 0
            self.simulation_state.stop_event.clear()
            
            # Start simulation in a separate thread
            self.simulation_state.thread = threading.Thread(
                target=self._run_simulation,
                args=(config.duration,),
                daemon=True
            )
            self.simulation_state.thread.start()
            
            self.logger.info(f"Started simulation with profile: {config.profile.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error starting simulation: {e}")
            self._cleanup_simulation()
            return False
    
    def stop_simulation(self) -> bool:
        """Stop the currently running simulation."""
        if not self.simulation_state.is_running:
            self.logger.warning("No simulation is currently running")
            return False
        
        try:
            # Signal the simulation thread to stop
            self.simulation_state.stop_event.set()
            
            # Stop the MQTT client
            if self.simulation_state.client:
                self.simulation_state.client.stop_simulation()
                self.simulation_state.client.disconnect()
            
            # Wait for thread to finish (with timeout)
            if self.simulation_state.thread and self.simulation_state.thread.is_alive():
                self.simulation_state.thread.join(timeout=5)
            
            self._cleanup_simulation()
            self.logger.info("Simulation stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"Error stopping simulation: {e}")
            return False
    
    def get_simulation_status(self) -> SimulationStatus:
        """Get the current simulation status."""
        return SimulationStatus(
            is_running=self.simulation_state.is_running,
            is_connected=self.simulation_state.is_connected,
            profile_name=self.simulation_state.config.profile.name if self.simulation_state.config else None,
            topic=self.simulation_state.client.profile.get_topic() if self.simulation_state.client and self.simulation_state.client.profile else None,
            interval=self.simulation_state.config.interval if self.simulation_state.config else None,
            messages_sent=self.simulation_state.messages_sent,
            start_time=self.simulation_state.start_time.isoformat() if self.simulation_state.start_time else None,
            last_message=self.simulation_state.last_message
        )
    
    def get_simulation_data(self, limit: int = 50) -> Dict[str, Any]:
        """Get recent simulation data."""
        messages = self._message_history[-limit:] if self._message_history else []
        return {
            "messages": messages,
            "total_count": self.simulation_state.messages_sent
        }
    
    def test_mqtt_connection(self, host: str, port: int, username: Optional[str] = None, password: Optional[str] = None) -> bool:
        """Test MQTT connection without starting simulation."""
        try:
            client = MQTTClient(
                broker_host=host,
                broker_port=port,
                username=username,
                password=password
            )
            
            connected = client.connect()
            client.disconnect()
            return connected
            
        except Exception as e:
            self.logger.error(f"Error testing MQTT connection: {e}")
            return False
    
    def _run_simulation(self, duration: Optional[int] = None):
        """Run the simulation in a separate thread."""
        try:
            start_time = time.time()
            
            while not self.simulation_state.stop_event.is_set():
                # Check duration
                if duration and (time.time() - start_time) > duration:
                    self.logger.info("Simulation duration reached")
                    break
                
                # Publish data
                if self.simulation_state.client and self.simulation_state.client.is_connected:
                    success = self.simulation_state.client.publish_data()
                    if success:
                        self.simulation_state.messages_sent += 1
                        
                        # Get the last published message
                        if self.simulation_state.client.profile:
                            data = self.simulation_state.client.profile.generate_data()
                            self.simulation_state.last_message = data
                            
                            # Add to history
                            message_record = {
                                "timestamp": datetime.utcnow().isoformat(),
                                "topic": self.simulation_state.client.profile.get_topic(),
                                "payload": data
                            }
                            self._message_history.append(message_record)
                            
                            # Keep only recent messages
                            if len(self._message_history) > self._max_history:
                                self._message_history.pop(0)
                
                # Sleep for the interval
                interval = self.simulation_state.config.interval if self.simulation_state.config else 5
                if self.simulation_state.stop_event.wait(interval):
                    break
                    
        except Exception as e:
            self.logger.error(f"Error in simulation thread: {e}")
        finally:
            self._cleanup_simulation()
    
    def _cleanup_simulation(self):
        """Clean up simulation state."""
        self.simulation_state.is_running = False
        self.simulation_state.is_connected = False
        self.simulation_state.client = None
        self.simulation_state.thread = None
        self.simulation_state.stop_event.clear()


# Global service instance
mqtt_service = MQTTService() 