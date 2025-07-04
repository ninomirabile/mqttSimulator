/**
 * Frontend Configuration
 * Centralized configuration for the MQTT Simulator frontend
 */

// API Configuration
export const API_CONFIG = {
    // Base URL for the API (change this for production)
    BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
    
    // Timeout for API requests (in milliseconds)
    TIMEOUT: 10000,
    
    // Retry configuration
    MAX_RETRIES: 3,
    RETRY_DELAY: 1000,
};

// MQTT Configuration
export const MQTT_CONFIG = {
    // Default MQTT settings
    DEFAULT_HOST: 'localhost',
    DEFAULT_PORT: 1883,
    DEFAULT_KEEPALIVE: 60,
    DEFAULT_QOS: 1,
    
    // Connection test timeout
    CONNECTION_TIMEOUT: 5000,
};

// UI Configuration
export const UI_CONFIG = {
    // Auto-refresh interval for status updates (in milliseconds)
    STATUS_REFRESH_INTERVAL: 1000,
    
    // Maximum number of messages to display
    MAX_MESSAGES: 100,
    
    // Auto-scroll threshold (percentage of container height)
    AUTO_SCROLL_THRESHOLD: 0.8,
};

// Development Configuration
export const DEV_CONFIG = {
    // Enable debug logging
    DEBUG: import.meta.env.DEV,
    
    // Mock data for development (when API is not available)
    USE_MOCK_DATA: false,
}; 