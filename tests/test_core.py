"""
Unit tests for MQTT Simulator core functionality.

This module contains tests for the MQTTClient class and related functionality.
"""

import pytest
import json
import time
from unittest.mock import Mock, patch
from mqtt_simulator.core import MQTTClient
from mqtt_simulator.profiles.weather import WeatherProfile


class TestMQTTClient:
    """Test cases for MQTTClient."""

    def test_mqtt_client_initialization(self):
        """Test MQTTClient initialization with default values."""
        client = MQTTClient()

        assert client.broker_host == "localhost"
        assert client.broker_port == 1883
        assert client.client_id.startswith("mqtt_simulator_")
        assert client.username is None
        assert client.password is None
        assert client.keepalive == 60
        assert not client.is_connected
        assert not client.is_running
        assert client.profile is None
        assert client.publish_interval == 5

    def test_mqtt_client_custom_config(self):
        """Test MQTTClient initialization with custom configuration."""
        client = MQTTClient(
            broker_host="test.broker.com",
            broker_port=8883,
            client_id="test_client",
            username="test_user",
            password="test_pass",
            keepalive=120,
            interval=10,
        )

        assert client.broker_host == "test.broker.com"
        assert client.broker_port == 8883
        assert client.client_id == "test_client"
        assert client.username == "test_user"
        assert client.password == "test_pass"
        assert client.keepalive == 120
        assert client.publish_interval == 10

    def test_mqtt_client_auto_client_id(self):
        """Test automatic client ID generation."""
        client1 = MQTTClient()
        client2 = MQTTClient()

        # Client IDs should have the correct format
        assert client1.client_id.startswith("mqtt_simulator_")
        assert client2.client_id.startswith("mqtt_simulator_")

        # Client IDs should contain a timestamp (numeric part)
        import re

        timestamp_pattern = r"mqtt_simulator_(\d+)"
        match1 = re.match(timestamp_pattern, client1.client_id)
        match2 = re.match(timestamp_pattern, client2.client_id)

        assert (
            match1 is not None
        ), f"Client ID {client1.client_id} doesn't match expected pattern"
        assert (
            match2 is not None
        ), f"Client ID {client2.client_id} doesn't match expected pattern"

        # The timestamp should be a reasonable value (not too old)
        timestamp1 = int(match1.group(1))
        timestamp2 = int(match2.group(1))
        current_time = int(time.time())

        # Timestamps should be within the last 10 seconds
        assert abs(current_time - timestamp1) < 10
        assert abs(current_time - timestamp2) < 10

    @patch("mqtt_simulator.core.mqtt.Client")
    def test_mqtt_client_connect_success(self, mock_mqtt_client):
        """Test successful MQTT connection."""
        # Mock the MQTT client
        mock_client_instance = Mock()
        mock_mqtt_client.return_value = mock_client_instance
        mock_client_instance.connect.return_value = 0

        client = MQTTClient()

        # Mock the connection callback to set is_connected to True
        def mock_on_connect(client, userdata, flags, rc):
            client._on_connect(client, userdata, flags, 0)

        mock_client_instance.on_connect = mock_on_connect

        # Mock the connection to immediately set is_connected
        def mock_connect(*args, **kwargs):
            client.is_connected = True
            return 0

        mock_client_instance.connect.side_effect = mock_connect

        # Test connection
        result = client.connect()

        assert result is True
        assert client.is_connected is True
        mock_client_instance.connect.assert_called_once_with(
            "localhost", 1883, 60
        )
        mock_client_instance.loop_start.assert_called_once()

    @patch("mqtt_simulator.core.mqtt.Client")
    def test_mqtt_client_connect_failure(self, mock_mqtt_client):
        """Test failed MQTT connection."""
        # Mock the MQTT client
        mock_client_instance = Mock()
        mock_mqtt_client.return_value = mock_client_instance
        mock_client_instance.connect.side_effect = Exception(
            "Connection failed"
        )

        client = MQTTClient()

        # Test connection failure
        result = client.connect()

        assert result is False
        assert client.is_connected is False

    @patch("mqtt_simulator.core.mqtt.Client")
    def test_mqtt_client_disconnect(self, mock_mqtt_client):
        """Test MQTT disconnection."""
        # Mock the MQTT client
        mock_client_instance = Mock()
        mock_mqtt_client.return_value = mock_client_instance

        client = MQTTClient()
        client.is_connected = True
        client.is_running = True

        client.disconnect()

        assert client.is_running is False
        mock_client_instance.loop_stop.assert_called_once()
        mock_client_instance.disconnect.assert_called_once()

    def test_set_profile(self):
        """Test setting a simulation profile."""
        client = MQTTClient()

        # Mock the get_profile function
        with patch("mqtt_simulator.core.get_profile") as mock_get_profile:
            mock_get_profile.return_value = WeatherProfile

            client.set_profile("weather", city="Test City")

            assert client.profile is not None
            assert isinstance(client.profile, WeatherProfile)
            assert client.profile.city == "Test City"
            assert client.publish_interval == 5  # Default interval

    def test_set_invalid_profile(self):
        """Test setting an invalid profile raises an error."""
        client = MQTTClient()

        # Mock the get_profile function to raise an error
        with patch("mqtt_simulator.core.get_profile") as mock_get_profile:
            mock_get_profile.side_effect = ValueError("Profile not found")

            with pytest.raises(ValueError, match="Profile not found"):
                client.set_profile("invalid_profile")

    @patch("mqtt_simulator.core.mqtt.Client")
    def test_publish_data_success(self, mock_mqtt_client):
        """Test successful data publishing."""
        # Mock the MQTT client
        mock_client_instance = Mock()
        mock_mqtt_client.return_value = mock_client_instance

        client = MQTTClient()
        client.is_connected = True
        client.profile = WeatherProfile(city="Test City")

        # Mock successful publish
        mock_result = Mock()
        mock_result.rc = 0  # MQTT_ERR_SUCCESS
        mock_client_instance.publish.return_value = mock_result

        result = client.publish_data()

        assert result is True
        mock_client_instance.publish.assert_called_once()

        # Check that publish was called with correct arguments
        call_args = mock_client_instance.publish.call_args
        assert call_args[0][0] == "weather/test_city"  # topic
        assert "Test City" in call_args[0][1]  # payload contains city
        # Check QoS - it should be passed as a keyword argument
        assert call_args[1]["qos"] == 1  # qos as keyword argument

    @patch("mqtt_simulator.core.mqtt.Client")
    def test_publish_data_not_connected(self, mock_mqtt_client):
        """Test publishing when not connected."""
        client = MQTTClient()
        client.is_connected = False
        client.profile = WeatherProfile()

        result = client.publish_data()

        assert result is False

    @patch("mqtt_simulator.core.mqtt.Client")
    def test_publish_data_no_profile(self, mock_mqtt_client):
        """Test publishing when no profile is set."""
        client = MQTTClient()
        client.is_connected = True
        client.profile = None

        result = client.publish_data()

        assert result is False

    @patch("mqtt_simulator.core.mqtt.Client")
    def test_publish_data_failure(self, mock_mqtt_client):
        """Test failed data publishing."""
        # Mock the MQTT client
        mock_client_instance = Mock()
        mock_mqtt_client.return_value = mock_client_instance

        client = MQTTClient()
        client.is_connected = True
        client.profile = WeatherProfile()

        # Mock failed publish
        mock_result = Mock()
        mock_result.rc = 1  # Some error
        mock_client_instance.publish.return_value = mock_result

        result = client.publish_data()

        assert result is False

    @patch("mqtt_simulator.core.mqtt.Client")
    def test_subscribe_success(self, mock_mqtt_client):
        """Test successful topic subscription."""
        # Mock the MQTT client
        mock_client_instance = Mock()
        mock_mqtt_client.return_value = mock_client_instance
        mock_client_instance.subscribe.return_value = (0, 1)  # (rc, mid)

        client = MQTTClient()
        client.is_connected = True

        result = client.subscribe("test/topic")

        assert result is True
        mock_client_instance.subscribe.assert_called_once_with("test/topic", 0)

    @patch("mqtt_simulator.core.mqtt.Client")
    def test_subscribe_not_connected(self, mock_mqtt_client):
        """Test subscription when not connected."""
        client = MQTTClient()
        client.is_connected = False

        result = client.subscribe("test/topic")

        assert result is False

    @patch("mqtt_simulator.core.mqtt.Client")
    def test_subscribe_failure(self, mock_mqtt_client):
        """Test failed topic subscription."""
        # Mock the MQTT client
        mock_client_instance = Mock()
        mock_mqtt_client.return_value = mock_client_instance
        mock_client_instance.subscribe.return_value = (1, 1)  # Error rc

        client = MQTTClient()
        client.is_connected = True

        result = client.subscribe("test/topic")

        assert result is False

    def test_start_simulation_no_profile(self):
        """Test starting simulation without a profile raises an error."""
        client = MQTTClient()
        client.profile = None

        with pytest.raises(ValueError, match="No profile set"):
            client.start_simulation()

    @patch("mqtt_simulator.core.time.sleep")
    @patch("mqtt_simulator.core.mqtt.Client")
    def test_start_simulation(self, mock_mqtt_client, mock_sleep):
        """Test simulation loop."""
        # Mock the MQTT client
        mock_client_instance = Mock()
        mock_mqtt_client.return_value = mock_client_instance

        client = MQTTClient()
        client.profile = WeatherProfile()
        client.is_running = True
        client.publish_interval = 1

        # Mock publish_data to return True and then stop the loop
        def mock_publish():
            client.is_running = False
            return True

        client.publish_data = mock_publish

        # Mock time.time to return increasing values
        with patch("mqtt_simulator.core.time.time") as mock_time:
            mock_time.side_effect = [0, 1, 2]  # Start time, then increasing

            client.start_simulation()

            # Verify sleep was called
            mock_sleep.assert_called_with(1)

    @patch("mqtt_simulator.core.time.sleep")
    @patch("mqtt_simulator.core.mqtt.Client")
    def test_start_simulation_with_duration(
        self, mock_mqtt_client, mock_sleep
    ):
        """Test simulation loop with duration limit."""
        # Mock the MQTT client
        mock_client_instance = Mock()
        mock_mqtt_client.return_value = mock_client_instance

        client = MQTTClient()
        client.profile = WeatherProfile()
        client.is_running = True
        client.publish_interval = 1

        # Mock publish_data to return True
        client.publish_data = Mock(return_value=True)

        # Mock time.time to simulate duration passing
        with patch("mqtt_simulator.core.time.time") as mock_time:
            mock_time.side_effect = [
                0,
                1,
                6,
            ]  # Start time, then after duration

            client.start_simulation(duration=5)

            # Verify sleep was called
            mock_sleep.assert_called_with(1)

    def test_stop_simulation(self):
        """Test stopping the simulation."""
        client = MQTTClient()
        client.is_running = True

        client.stop_simulation()

        assert client.is_running is False


class TestMQTTCallbacks:
    """Test cases for MQTT callback functions."""

    def test_on_connect_success(self):
        """Test successful connection callback."""
        client = MQTTClient()

        # Test successful connection
        client._on_connect(None, None, None, 0)

        assert client.is_connected is True

    def test_on_connect_failure(self):
        """Test failed connection callback."""
        client = MQTTClient()

        # Test failed connection
        client._on_connect(None, None, None, 1)

        assert client.is_connected is False

    def test_on_disconnect_normal(self):
        """Test normal disconnection callback."""
        client = MQTTClient()
        client.is_connected = True

        # Test normal disconnection
        client._on_disconnect(None, None, 0)

        assert client.is_connected is False

    def test_on_disconnect_unexpected(self):
        """Test unexpected disconnection callback."""
        client = MQTTClient()
        client.is_connected = True

        # Test unexpected disconnection
        client._on_disconnect(None, None, 1)

        assert client.is_connected is False

    def test_on_publish(self):
        """Test publish callback."""
        client = MQTTClient()

        # This should not raise any errors
        client._on_publish(None, None, 123)

    def test_on_message_valid_json(self):
        """Test message callback with valid JSON."""
        client = MQTTClient()

        # Mock message with valid JSON
        mock_msg = Mock()
        mock_msg.topic = "test/topic"
        mock_msg.payload = json.dumps({"test": "data"}).encode()

        # This should not raise any errors
        client._on_message(None, None, mock_msg)

    def test_on_message_invalid_json(self):
        """Test message callback with invalid JSON."""
        client = MQTTClient()

        # Mock message with invalid JSON
        mock_msg = Mock()
        mock_msg.topic = "test/topic"
        mock_msg.payload = b"invalid json"

        # This should not raise any errors
        client._on_message(None, None, mock_msg)
