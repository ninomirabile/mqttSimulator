# Contributing to MQTT Simulator

Thank you for your interest in contributing to MQTT Simulator! This document provides guidelines and information for contributors.

## Development Setup

### Prerequisites

- Python 3.10+
- Node.js 16+
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mqtt-simulator.git
   cd mqtt-simulator
   ```

2. **Start development environment (Recommended)**
   ```bash
   # Make the script executable (first time only)
   chmod +x start.sh
   
   # Start the entire development stack
   ./start.sh
   ```
   
   This will install all dependencies and start both API and frontend servers.

3. **Alternative: Manual setup**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-api.txt
   
   # Frontend dependencies
   cd frontend
   npm install
   cd ..
   
   # Start API (in one terminal)
   python3 -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
   
   # Start frontend (in another terminal)
   cd frontend
   npm run dev
   ```

4. **Run tests**
   ```bash
   # Python tests
   pytest
   
   # Integration tests
   python3 test_integration.py
   
   # Frontend tests
   cd frontend
   npm run check
   ```

## Project Structure

```
mqtt-simulator/
├── mqtt_simulator/          # Core Python library
│   ├── __init__.py
│   ├── core.py              # MQTT client implementation
│   ├── cli.py               # Command-line interface
│   └── profiles/            # Data simulation profiles
│       ├── __init__.py
│       ├── base.py          # Base profile class
│       ├── weather.py       # Weather data simulator
│       ├── agriculture.py   # Agriculture data simulator
│       └── energy.py        # Energy data simulator
├── api/                     # FastAPI REST API
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── routes/              # API endpoints
│   └── services/            # Business logic
├── frontend/                # Svelte web application
│   ├── src/
│   │   ├── lib/             # Shared components and utilities
│   │   ├── routes/          # SvelteKit routes
│   │   └── app.css          # Global styles
│   ├── package.json
│   └── svelte.config.js
├── tests/                   # Test suite
├── examples/                # Usage examples
└── docs/                    # Documentation
```

## Adding New Profiles

### 1. Create Profile Module

Create a new file in `mqtt_simulator/profiles/` (e.g., `traffic.py`):

```python
from pydantic import BaseModel
from datetime import datetime
import random

class TrafficData(BaseModel):
    sensor_id: str
    vehicle_count: int
    average_speed: float
    congestion_level: str
    timestamp: datetime

class TrafficSimulator:
    """Traffic data simulation profile."""
    
    def __init__(self, sensor_id: str = "traffic-001"):
        self.sensor_id = sensor_id
        self.config = {
            "sensor_id": "Traffic sensor identifier",
            "base_vehicle_count": "Base number of vehicles",
            "base_speed": "Base average speed in km/h"
        }
    
    def generate_data(self) -> dict:
        """Generate traffic data."""
        return TrafficData(
            sensor_id=self.sensor_id,
            vehicle_count=random.randint(0, 100),
            average_speed=random.uniform(20, 80),
            congestion_level=random.choice(["low", "medium", "high"]),
            timestamp=datetime.utcnow()
        ).dict()
    
    def get_topic(self) -> str:
        """Get MQTT topic for traffic data."""
        return f"traffic/{self.sensor_id}"
```

### 2. Register Profile

Add the profile to `mqtt_simulator/profiles/__init__.py`:

```python
from .traffic import TrafficSimulator

_PROFILES = {
    "weather": WeatherSimulator,
    "agriculture": AgricultureSimulator,
    "energy": EnergySimulator,
    "traffic": TrafficSimulator,  # Add your profile
}
```

### 3. Write Tests

Create tests in `tests/test_profiles.py`:

```python
def test_traffic_profile():
    """Test traffic profile data generation."""
    profile = TrafficSimulator(sensor_id="test-001")
    data = profile.generate_data()
    
    assert data["sensor_id"] == "test-001"
    assert "vehicle_count" in data
    assert "average_speed" in data
    assert "congestion_level" in data
    assert "timestamp" in data
```

### 4. Update Documentation

- Add profile description to README.md
- Include example payload
- Document any configuration options

## Code Style

### Python

- Use **Black** for code formatting
- Use **Flake8** for linting
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for all public functions

```bash
# Format code
black mqtt_simulator/ tests/

# Lint code
flake8 mqtt_simulator/ tests/
```

### JavaScript/Svelte

- Use **Prettier** for formatting
- Use **ESLint** for linting
- Follow Svelte best practices
- Use TypeScript for type safety

```bash
cd frontend
npm run format
npm run lint
```

## Testing

### Python Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=mqtt_simulator

# Run specific test file
pytest tests/test_profiles.py

# Run with verbose output
pytest -v
```

### Frontend Tests

```bash
cd frontend
npm run check
```

### Integration Tests

```bash
python3 test_integration.py
```

## API Development

### Adding New Endpoints

1. **Create route file** in `api/routes/`
2. **Add Pydantic models** in `api/models.py`
3. **Register route** in `api/main.py`
4. **Write tests** for the endpoint

### Example Endpoint

```python
# api/routes/example.py
from fastapi import APIRouter, HTTPException
from ..models import ExampleRequest, ExampleResponse

router = APIRouter(prefix="/example", tags=["example"])

@router.post("/", response_model=ExampleResponse)
async def create_example(request: ExampleRequest):
    """Create a new example."""
    try:
        # Your logic here
        return ExampleResponse(success=True, data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Frontend Development

### Adding New Components

1. **Create component** in `frontend/src/lib/components/`
2. **Add to store** if needed in `frontend/src/lib/stores/`
3. **Import and use** in pages

### Example Component

```svelte
<!-- frontend/src/lib/components/Example.svelte -->
<script>
    export let data = null;
    
    function handleClick() {
        // Component logic
    }
</script>

<div class="example-component">
    {#if data}
        <p>{data}</p>
    {/if}
    <button on:click={handleClick}>Click me</button>
</div>

<style>
    .example-component {
        padding: 1rem;
        border: 1px solid #ccc;
        border-radius: 0.5rem;
    }
</style>
```

## Pull Request Process

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Write/update tests**
5. **Run the test suite**
   ```bash
   pytest
   cd frontend && npm run check
   ```
6. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
7. **Push to your branch**
   ```bash
   git push origin feature/amazing-feature
   ```
8. **Create a Pull Request**

### PR Guidelines

- **Title**: Clear, descriptive title
- **Description**: Explain what the PR does and why
- **Tests**: Ensure all tests pass
- **Documentation**: Update docs if needed
- **Screenshots**: Include screenshots for UI changes

## Issue Reporting

When reporting issues, please include:

- **OS and version**
- **Python version**
- **Node.js version**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Error messages/logs**

## Code of Conduct

- Be respectful and inclusive
- Help others learn
- Provide constructive feedback
- Follow the project's coding standards

## Getting Help

- **Issues**: Use GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub discussions for questions
- **Documentation**: Check the README and API docs

## License

By contributing, you agree that your contributions will be licensed under the MIT License. 