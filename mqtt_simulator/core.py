"""
Core MQTT Client - Main MQTT functionality for the simulator.

This module provides the core MQTT client functionality including connection,
publishing, subscription, and message handling.
"""

import json
import time
import logging
from typing import Optional, Callable, Dict, Any
from datetime import datetime
import paho.mqtt.client as mqtt
from .profiles import get_profile, BaseProfile


class MQTTClient:
    """MQTT client for publishing simulated data."""
    
    def __init__(
        self,
        broker_host: str = "localhost",
        broker_port: int = 1883,
        client_id: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        keepalive: int = 60,
        **kwargs
    ):
        """Initialize the MQTT client."""
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client_id = client_id or f"mqtt_simulator_{int(time.time())}"
        self.username = username
        self.password = password
        self.keepalive = keepalive
        
        # MQTT client setup
        self.client = mqtt.Client(
            client_id=self.client_id,
            clean_session=True,
            protocol=mqtt.MQTTv311
        )
        
        # Set up authentication if provided
        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)
        
        # Set up callbacks
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_publish = self._on_publish
        self.client.on_message = self._on_message
        
        # Connection state
        self.is_connected = False
        self.is_running = False
        
        # Profile and configuration
        self.profile: Optional[BaseProfile] = None
        self.publish_interval = kwargs.get("interval", 5)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _on_connect(self, client, userdata, flags, rc):
        """Callback for when the client connects to the broker."""
        if rc == 0:
            self.is_connected = True
            self.logger.info(f"Connected to MQTT broker at {self.broker_host}:{self.broker_port}")
        else:
            self.logger.error(f"Failed to connect to MQTT broker. Return code: {rc}")
    
    def _on_disconnect(self, client, userdata, rc):
        """Callback for when the client disconnects from the broker."""
        self.is_connected = False
        if rc != 0:
            self.logger.warning(f"Unexpected disconnection. Return code: {rc}")
        else:
            self.logger.info("Disconnected from MQTT broker")
    
    def _on_publish(self, client, userdata, mid):
        """Callback for when a message is published."""
        self.logger.debug(f"Message published with ID: {mid}")
    
    def _on_message(self, client, userdata, msg):
        """Callback for when a message is received."""
        try:
            payload = json.loads(msg.payload.decode())
            self.logger.info(f"Received message on {msg.topic}: {payload}")
        except json.JSONDecodeError:
            self.logger.warning(f"Received non-JSON message on {msg.topic}")
    
    def connect(self) -> bool:
        """Connect to the MQTT broker."""
        try:
            self.client.connect(self.broker_host, self.broker_port, self.keepalive)
            self.client.loop_start()
            
            # Wait for connection
            timeout = 10
            start_time = time.time()
            while not self.is_connected and (time.time() - start_time) < timeout:
                time.sleep(0.1)
            
            return self.is_connected
        except Exception as e:
            self.logger.error(f"Failed to connect to MQTT broker: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the MQTT broker."""
        if self.is_connected:
            self.is_running = False
            self.client.loop_stop()
            self.client.disconnect()
            self.logger.info("Disconnected from MQTT broker")
    
    def set_profile(self, profile_name: str, **profile_config):
        """Set the simulation profile."""
        try:
            profile_class = get_profile(profile_name)
            self.profile = profile_class(**profile_config)
            self.publish_interval = self.profile.get_interval()
            self.logger.info(f"Set profile: {profile_name}")
        except ValueError as e:
            self.logger.error(f"Failed to set profile: {e}")
            raise
    
    def publish_data(self):
        """Publish simulated data to MQTT broker."""
        if not self.is_connected or not self.profile:
            return False
        
        try:
            topic = self.profile.get_topic()
            payload = self.profile.get_payload()
            
            result = self.client.publish(topic, payload, qos=1)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                self.logger.info(f"Published to {topic}: {payload}")
                return True
            else:
                self.logger.error(f"Failed to publish message: {result.rc}")
                return False
        except Exception as e:
            self.logger.error(f"Error publishing data: {e}")
            return False
    
    def start_simulation(self, duration: Optional[int] = None):
        """Start the simulation loop."""
        if not self.profile:
            raise ValueError("No profile set. Use set_profile() first.")
        
        self.is_running = True
        start_time = time.time()
        
        self.logger.info(f"Starting simulation with profile: {self.profile.__class__.__name__}")
        self.logger.info(f"Publishing to topic: {self.profile.get_topic()}")
        self.logger.info(f"Interval: {self.publish_interval} seconds")
        
        try:
            while self.is_running:
                if duration and (time.time() - start_time) > duration:
                    self.logger.info("Simulation duration reached, stopping...")
                    break
                
                self.publish_data()
                time.sleep(self.publish_interval)
                
        except KeyboardInterrupt:
            self.logger.info("Simulation interrupted by user")
        finally:
            self.is_running = False
    
    def stop_simulation(self):
        """Stop the simulation loop."""
        self.is_running = False
        self.logger.info("Stopping simulation...")
    
    def subscribe(self, topic: str, qos: int = 0):
        """Subscribe to a topic."""
        if not self.is_connected:
            self.logger.error("Not connected to broker")
            return False
        
        result = self.client.subscribe(topic, qos)
        if result[0] == mqtt.MQTT_ERR_SUCCESS:
            self.logger.info(f"Subscribed to topic: {topic}")
            return True
        else:
            self.logger.error(f"Failed to subscribe to topic: {topic}")
            return False 