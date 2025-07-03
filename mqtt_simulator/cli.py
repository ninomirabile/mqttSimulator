"""
CLI Interface - Command-line interface for the MQTT Simulator.

This module provides a command-line interface for running simulations
with different profiles and configurations.
"""

import os
import sys
import click
from typing import Optional
from dotenv import load_dotenv
from .core import MQTTClient
from .profiles import get_available_profiles


# Load environment variables
load_dotenv()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """MQTT Simulator - Simulate real-time data publishing via MQTT."""
    pass


@cli.command()
@click.option("--profile", "-p", required=True, help="Simulation profile to use")
@click.option("--broker", "-b", default="localhost", help="MQTT broker host")
@click.option("--port", default=1883, help="MQTT broker port")
@click.option("--username", help="MQTT broker username")
@click.option("--password", help="MQTT broker password")
@click.option("--interval", "-i", default=5, help="Publishing interval in seconds")
@click.option("--duration", "-d", help="Simulation duration in seconds")
@click.option("--city", help="City name (for weather profile)")
@click.option("--sensor-id", help="Sensor ID (for agriculture profile)")
@click.option("--meter-id", help="Meter ID (for energy profile)")
@click.option("--load-pattern", type=click.Choice(["residential", "commercial", "industrial"]), 
              help="Load pattern (for energy profile)")
@click.option("--soil-type", type=click.Choice(["sandy", "clay", "loam"]), 
              help="Soil type (for agriculture profile)")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
def run(profile, broker, port, username, password, interval, duration, 
        city, sensor_id, meter_id, load_pattern, soil_type, verbose):
    """Run a simulation with the specified profile."""
    
    # Set up logging level
    if verbose:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Get available profiles
    available_profiles = get_available_profiles()
    
    if profile not in available_profiles:
        click.echo(f"Error: Profile '{profile}' not found.")
        click.echo(f"Available profiles: {', '.join(available_profiles.keys())}")
        sys.exit(1)
    
    # Build profile configuration
    profile_config = {"interval": interval}
    
    if city:
        profile_config["city"] = city
    if sensor_id:
        profile_config["sensor_id"] = sensor_id
    if meter_id:
        profile_config["meter_id"] = meter_id
    if load_pattern:
        profile_config["load_pattern"] = load_pattern
    if soil_type:
        profile_config["soil_type"] = soil_type
    
    # Get credentials from environment if not provided
    username = username or os.getenv("MQTT_USERNAME")
    password = password or os.getenv("MQTT_PASSWORD")
    
    try:
        # Create and configure MQTT client
        client = MQTTClient(
            broker_host=broker,
            broker_port=port,
            username=username,
            password=password
        )
        
        # Set the profile
        client.set_profile(profile, **profile_config)
        
        # Connect to broker
        click.echo(f"Connecting to MQTT broker at {broker}:{port}...")
        if not client.connect():
            click.echo("Error: Failed to connect to MQTT broker.")
            sys.exit(1)
        
        click.echo(f"Connected! Starting simulation with {profile} profile...")
        click.echo(f"Publishing to topic: {client.profile.get_topic()}")
        click.echo(f"Interval: {interval} seconds")
        if duration:
            click.echo(f"Duration: {duration} seconds")
        click.echo("Press Ctrl+C to stop...")
        
        # Start simulation
        client.start_simulation(duration=duration)
        
    except KeyboardInterrupt:
        click.echo("\nSimulation stopped by user.")
    except Exception as e:
        click.echo(f"Error: {e}")
        sys.exit(1)
    finally:
        if 'client' in locals():
            client.disconnect()


@cli.command()
def list_profiles():
    """List all available simulation profiles."""
    profiles = get_available_profiles()
    
    click.echo("Available simulation profiles:")
    click.echo()
    
    for name, profile_class in profiles.items():
        click.echo(f"  {name}: {profile_class.__doc__ or 'No description'}")
    
    click.echo()
    click.echo("Use 'mqtt-simulator run --profile <name>' to run a simulation.")


@cli.command()
@click.argument("profile")
def show_profile(profile):
    """Show details about a specific profile."""
    profiles = get_available_profiles()
    
    if profile not in profiles:
        click.echo(f"Error: Profile '{profile}' not found.")
        click.echo(f"Available profiles: {', '.join(profiles.keys())}")
        sys.exit(1)
    
    profile_class = profiles[profile]
    
    click.echo(f"Profile: {profile}")
    click.echo(f"Class: {profile_class.__name__}")
    click.echo(f"Description: {profile_class.__doc__ or 'No description'}")
    click.echo()
    
    # Show example data
    try:
        instance = profile_class()
        example_data = instance.generate_data()
        example_topic = instance.get_topic()
        
        click.echo("Example topic:")
        click.echo(f"  {example_topic}")
        click.echo()
        click.echo("Example payload:")
        click.echo(f"  {instance.get_payload()}")
        
    except Exception as e:
        click.echo(f"Error generating example: {e}")


@cli.command()
@click.option("--broker", "-b", default="localhost", help="MQTT broker host")
@click.option("--port", default=1883, help="MQTT broker port")
@click.option("--username", help="MQTT broker username")
@click.option("--password", help="MQTT broker password")
@click.option("--topic", "-t", help="Topic to subscribe to")
def subscribe(broker, port, username, password, topic):
    """Subscribe to MQTT topics and listen for messages."""
    
    # Get credentials from environment if not provided
    username = username or os.getenv("MQTT_USERNAME")
    password = password or os.getenv("MQTT_PASSWORD")
    
    try:
        client = MQTTClient(
            broker_host=broker,
            broker_port=port,
            username=username,
            password=password
        )
        
        click.echo(f"Connecting to MQTT broker at {broker}:{port}...")
        if not client.connect():
            click.echo("Error: Failed to connect to MQTT broker.")
            sys.exit(1)
        
        if topic:
            client.subscribe(topic)
            click.echo(f"Subscribed to topic: {topic}")
        else:
            # Subscribe to all simulator topics
            topics = ["weather/#", "agriculture/#", "energy/#"]
            for t in topics:
                client.subscribe(t)
                click.echo(f"Subscribed to topic: {t}")
        
        click.echo("Listening for messages... Press Ctrl+C to stop.")
        
        # Keep the client running
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            click.echo("\nStopping subscription...")
            
    except Exception as e:
        click.echo(f"Error: {e}")
        sys.exit(1)
    finally:
        if 'client' in locals():
            client.disconnect()


if __name__ == "__main__":
    cli() 