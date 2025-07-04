"""
FastAPI Application - Main entry point for the MQTT Simulator API.

This module provides the FastAPI application with all routes and middleware
for the MQTT Simulator web API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from .routes import simulation, profiles, mqtt
from .models import APIResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="MQTT Simulator API",
    description="API for controlling MQTT data simulation with various profiles",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(simulation.router, prefix="/api")
app.include_router(profiles.router, prefix="/api")
app.include_router(mqtt.router, prefix="/api")


@app.get("/", response_model=APIResponse)
async def root():
    """Root endpoint with API information."""
    endpoints = {
        "simulation": "/api/simulation",
        "profiles": "/api/profiles",
        "mqtt": "/api/mqtt",
    }
    data = {
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": endpoints
    }
    return APIResponse(
        success=True,
        message="MQTT Simulator API is running",
        data=data
    )


@app.get("/health", response_model=APIResponse)
async def health_check():
    """Health check endpoint."""
    return APIResponse(
        success=True, message="API is healthy", data={"status": "ok"}
    )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "details": str(exc) if str(exc) else "Unknown error",
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
