# Examples

This directory contains examples and demonstrations of the MQTT Simulator.

## Available Examples

### web_interface_demo.py

A comprehensive demonstration script for the web interface.

**Features:**
- Automatic MQTT broker detection and startup
- API health checking
- Step-by-step web interface instructions
- Example configurations for all profiles
- API testing examples with curl
- Troubleshooting guide

**Usage:**
```bash
python3 examples/web_interface_demo.py
```

**What it does:**
1. Checks if MQTT broker is running (tries to start Mosquitto if needed)
2. Verifies API is accessible
3. Provides detailed instructions for using the web interface
4. Shows example configurations for weather, agriculture, and energy profiles
5. Includes curl examples for API testing
6. Offers troubleshooting tips

**Prerequisites:**
- Python 3.10+
- MQTT broker (Mosquitto recommended)
- API server running on port 8000
- Frontend server running on port 5173

## Running Examples

### Quick Start
```bash
# Start the development environment
./start.sh

# In another terminal, run the demo
python3 examples/web_interface_demo.py
```

### Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt requirements-api.txt

# Start API
python3 -m uvicorn api.main:app --reload --port 8000

# Start frontend (in another terminal)
cd frontend && npm run dev

# Run demo (in another terminal)
python3 examples/web_interface_demo.py
```

## Example Configurations

### Weather Profile
```json
{
  "profile": "weather",
  "city": "Milano",
  "topic": "weather/milano",
  "interval": 5
}
```

### Agriculture Profile
```json
{
  "profile": "agriculture",
  "sensor_id": "soil-001",
  "topic": "agriculture/soil/soil-001",
  "interval": 10
}
```

### Energy Profile
```json
{
  "profile": "energy",
  "meter_id": "energy-01",
  "topic": "energy/meter/energy-01",
  "interval": 3
}
```

## API Examples

### Get Available Profiles
```bash
curl http://localhost:8000/api/profiles/
```

### Start Simulation
```bash
curl -X POST http://localhost:8000/api/simulation/start \
  -H 'Content-Type: application/json' \
  -d '{
    "profile": "weather",
    "mqtt_config": {
      "host": "localhost",
      "port": 1883
    },
    "profile_config": {
      "city": "Milano"
    },
    "interval": 5
  }'
```

### Test MQTT Connection
```bash
curl -X POST http://localhost:8000/api/mqtt/connect \
  -H 'Content-Type: application/json' \
  -d '{
    "host": "localhost",
    "port": 1883
  }'
```

## Contributing Examples

To add new examples:

1. Create a new Python file in this directory
2. Include a descriptive docstring
3. Add error handling and user-friendly output
4. Update this README with documentation
5. Test the example thoroughly

## Troubleshooting

### Common Issues

**MQTT Broker Not Found:**
- Install Mosquitto: `sudo apt install mosquitto mosquitto-clients`
- Or use a cloud MQTT broker (HiveMQ, AWS IoT, etc.)

**API Not Responding:**
- Check if API server is running on port 8000
- Restart with: `python3 -m uvicorn api.main:app --reload --port 8000`

**Frontend Not Loading:**
- Check if frontend server is running on port 5173
- Start with: `cd frontend && npm run dev`

**CORS Errors:**
- API should allow all origins in development mode
- Check API configuration in `api/main.py` 