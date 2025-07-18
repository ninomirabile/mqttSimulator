# MQTT Simulator - Project Status

## Overview

MQTT Simulator is a comprehensive tool for simulating real-time data publishing via MQTT protocol. It provides both a Python library and a modern web interface for easy data simulation.

## Current Status

### ✅ Completed Features

#### Core Library
- **MQTT Client**: Full MQTT protocol support (connect, publish, subscribe, disconnect)
- **Profile System**: Modular data generation with configurable profiles
- **CLI Interface**: Command-line tool for quick simulations
- **Python Library**: Usable as a library in Python projects

#### Web Interface
- **Modern Dashboard**: Svelte-based web interface with beautiful UI
- **Dynamic Profile Forms**: Form fields that adapt based on selected profile
- **Live Payload Preview**: Real-time preview of generated data
- **MQTT Configuration**: Complete MQTT broker configuration
- **Connection Testing**: Test MQTT connections before starting simulations
- **Live Data View**: Real-time display of published messages
- **Status Monitoring**: Clear visual feedback for connection and simulation status

#### Profiles Available
- **Weather**: Temperature, humidity, wind speed, conditions
- **Agriculture**: Soil moisture, temperature, pH levels
- **Energy**: Power consumption, voltage, current, frequency

#### Development Tools
- **Startup Script**: `start.sh` for easy development setup
- **Docker Support**: `docker-compose.yml` for containerized deployment
- **Integration Tests**: `test_integration.py` for end-to-end testing
- **API Documentation**: Interactive docs at `/docs` endpoint

### 🔧 Development Infrastructure

#### Testing
- Unit tests with pytest
- Integration tests for complete system
- Coverage reporting
- Linting with flake8

#### Documentation
- Comprehensive README with examples
- API documentation with FastAPI
- Contributing guidelines
- Docker configuration docs

#### Deployment
- Docker Compose setup
- Development startup script
- Production-ready configuration

## Architecture

```
mqtt-simulator/
├── mqtt_simulator/          # Core Python library
│   ├── core.py              # MQTT client implementation
│   ├── cli.py               # Command-line interface
│   └── profiles/            # Data simulation profiles
├── api/                     # FastAPI REST API
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── routes/              # API endpoints
│   └── services/            # Business logic
├── frontend/                # Svelte web application
│   ├── src/                 # Source code
│   ├── static/              # Static assets
│   └── package.json         # Dependencies
├── tests/                   # Test suite
├── examples/                # Usage examples
├── docs/                    # Documentation
├── start.sh                 # Development startup script
├── docker-compose.yml       # Docker configuration
└── test_integration.py      # Integration tests
```

## Quick Start Options

### 1. Development (Recommended)
```bash
./start.sh
```

### 2. Docker
```bash
docker-compose up -d
```

### 3. Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt requirements-api.txt
cd frontend && npm install

# Start services
python3 -m uvicorn api.main:app --reload --port 8000
cd frontend && npm run dev
```

## API Endpoints

### Simulation Control
- `POST /api/simulation/start` - Start simulation
- `POST /api/simulation/stop` - Stop simulation
- `GET /api/simulation/status` - Get status
- `GET /api/simulation/data` - Get recent data

### Profile Management
- `GET /api/profiles/` - List profiles
- `GET /api/profiles/{name}` - Get profile details
- `POST /api/profiles/{name}/preview` - Generate preview

### MQTT Connection
- `POST /api/mqtt/connect` - Test connection
- `GET /api/mqtt/status` - Get connection status

## Testing

### Run All Tests
```bash
pytest
python3 test_integration.py
```

### Development Testing
```bash
# Start services
./start.sh

# In another terminal
python3 test_integration.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Update documentation
6. Submit a pull request

## License

Creative Commons Attribution-NonCommercial 4.0 International License

## Author

Antonino Mirabile

## Support

- **Issues**: GitHub Issues
- **Documentation**: API docs at `/docs`
- **Examples**: `examples/` directory 