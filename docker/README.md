# Docker Configuration

This directory contains Docker configuration files for running the MQTT Simulator in containers.

## Overview

The Docker setup includes:
- **MQTT Broker**: Mosquitto MQTT broker for testing
- **API**: FastAPI backend service
- **Frontend**: Svelte web application
- **MQTT Client**: Test client for monitoring messages

## Quick Start

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

## Services

### MQTT Broker (Mosquitto)
- **Port**: 1883 (MQTT), 9001 (WebSocket)
- **Image**: eclipse-mosquitto:2.0
- **Purpose**: Provides MQTT broker for testing

### API Service
- **Port**: 8000
- **Purpose**: FastAPI backend with MQTT simulation logic
- **Dependencies**: MQTT Broker

### Frontend Service
- **Port**: 5173
- **Purpose**: Svelte web interface
- **Dependencies**: API Service

### MQTT Client (Test)
- **Purpose**: Subscribes to all topics for monitoring
- **Dependencies**: MQTT Broker

## Configuration Files

The following configuration files need to be created:

### Mosquitto Configuration
Create `docker/mosquitto/config/mosquitto.conf`:
```conf
listener 1883
allow_anonymous true
persistence true
persistence_location /mosquitto/data/
log_dest file /mosquitto/log/mosquitto.log
```

### API Dockerfile
Create `docker/api/Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements-api.txt ./
RUN pip install -r requirements.txt -r requirements-api.txt

COPY mqtt_simulator/ ./mqtt_simulator/
COPY api/ ./api/

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile
Create `docker/frontend/Dockerfile`:
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

## Usage

1. **Development**: Use `docker-compose up -d` for development
2. **Production**: Build and deploy individual services
3. **Testing**: Use the included MQTT client for message monitoring

## Troubleshooting

- **Port conflicts**: Ensure ports 1883, 8000, and 5173 are available
- **Permission issues**: Create necessary directories with proper permissions
- **Network issues**: Check if the mqtt-simulator-network is created properly

## Environment Variables

- `MQTT_BROKER_HOST`: MQTT broker hostname (default: mqtt-broker)
- `MQTT_BROKER_PORT`: MQTT broker port (default: 1883)
- `VITE_API_URL`: API URL for frontend (default: http://localhost:8000/api) 