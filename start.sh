#!/bin/bash

# MQTT Simulator Startup Script
# This script starts the entire MQTT Simulator stack
#
# Features:
# - Automatic dependency installation (Python + Node.js)
# - Health checks for prerequisites
# - Service startup with status monitoring
# - Graceful shutdown handling
# - Color-coded output for better UX
# - Port availability checking
# - Service readiness waiting
#
# Usage:
#     ./start.sh
#
# Prerequisites:
#     - Python 3.10+
#     - Node.js 16+
#     - Git
#
# The script will:
# 1. Check prerequisites
# 2. Install Python dependencies
# 3. Install frontend dependencies
# 4. Start API server (port 8000)
# 5. Start frontend server (port 5173)
# 6. Provide status and URLs
# 7. Handle cleanup on Ctrl+C
#
# Services started:
# - API: http://localhost:8000
# - Frontend: http://localhost:5173
# - API Docs: http://localhost:8000/docs

set -e

echo "🚀 Starting MQTT Simulator..."
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a port is in use
port_in_use() {
    lsof -i :$1 >/dev/null 2>&1
}

# Function to wait for a service to be ready
wait_for_service() {
    local host=$1
    local port=$2
    local service_name=$3
    
    echo -e "${BLUE}Waiting for $service_name to be ready...${NC}"
    for i in {1..30}; do
        if nc -z $host $port 2>/dev/null; then
            echo -e "${GREEN}✅ $service_name is ready!${NC}"
            return 0
        fi
        echo -n "."
        sleep 1
    done
    echo -e "${RED}❌ $service_name failed to start${NC}"
    return 1
}

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

if ! command_exists python3; then
    echo -e "${RED}❌ Python 3 is required but not installed${NC}"
    exit 1
fi

if ! command_exists npm; then
    echo -e "${RED}❌ Node.js/npm is required but not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"

# Install Python dependencies
echo -e "${BLUE}Installing Python dependencies...${NC}"
pip install -r requirements.txt
pip install -r requirements-api.txt
echo -e "${GREEN}✅ Python dependencies installed${NC}"

# Install frontend dependencies
echo -e "${BLUE}Installing frontend dependencies...${NC}"
cd frontend
npm install
cd ..
echo -e "${GREEN}✅ Frontend dependencies installed${NC}"

# Check if MQTT broker is needed
if ! port_in_use 1883; then
    echo -e "${YELLOW}⚠️  No MQTT broker found on port 1883${NC}"
    echo -e "${BLUE}You can install Mosquitto with:${NC}"
    echo "   Ubuntu/Debian: sudo apt install mosquitto"
    echo "   macOS: brew install mosquitto"
    echo "   Or use any other MQTT broker (HiveMQ, AWS IoT, etc.)"
    echo ""
    echo -e "${YELLOW}The simulator will work without a broker for testing the web interface${NC}"
    echo ""
fi

# Start API in background
echo -e "${BLUE}Starting API server...${NC}"
if port_in_use 8000; then
    echo -e "${YELLOW}⚠️  Port 8000 is already in use. API might already be running.${NC}"
else
    python3 -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000 &
    API_PID=$!
    echo -e "${GREEN}✅ API server started (PID: $API_PID)${NC}"
fi

# Wait for API to be ready
wait_for_service localhost 8000 "API"

# Start frontend in background
echo -e "${BLUE}Starting frontend development server...${NC}"
if port_in_use 5173; then
    echo -e "${YELLOW}⚠️  Port 5173 is already in use. Frontend might already be running.${NC}"
else
    cd frontend
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    echo -e "${GREEN}✅ Frontend server started (PID: $FRONTEND_PID)${NC}"
fi

# Wait for frontend to be ready
wait_for_service localhost 5173 "Frontend"

# Display status
echo ""
echo -e "${GREEN}🎉 MQTT Simulator is ready!${NC}"
echo "================================"
echo -e "${BLUE}📱 Web Interface:${NC} http://localhost:5173"
echo -e "${BLUE}🔧 API Documentation:${NC} http://localhost:8000/docs"
echo -e "${BLUE}🌐 API Base URL:${NC} http://localhost:8000"
echo ""
echo -e "${YELLOW}To stop the services, press Ctrl+C${NC}"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${BLUE}🛑 Stopping services...${NC}"
    
    if [ ! -z "$API_PID" ]; then
        kill $API_PID 2>/dev/null || true
        echo -e "${GREEN}✅ API server stopped${NC}"
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
        echo -e "${GREEN}✅ Frontend server stopped${NC}"
    fi
    
    echo -e "${GREEN}✅ All services stopped${NC}"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Keep script running
echo ""
echo -e "${BLUE}Services are running. Press Ctrl+C to stop.${NC}"
while true; do
    sleep 1
done 