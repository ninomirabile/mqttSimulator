/**
 * API Client for MQTT Simulator Backend
 * Handles all communication with the FastAPI backend
 */

import { API_CONFIG } from './config.js';

class ApiClient {
    constructor() {
        this.baseUrl = API_CONFIG.BASE_URL;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            ...options,
        };

        // Add timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), API_CONFIG.TIMEOUT);
        config.signal = controller.signal;

        try {
            const response = await fetch(url, config);
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            clearTimeout(timeoutId);
            
            if (error.name === 'AbortError') {
                throw new Error('Request timeout');
            }
            
            console.error(`API request failed: ${error.message}`);
            throw error;
        }
    }

    // Simulation endpoints
    async startSimulation(config) {
        return this.request('/simulation/start', {
            method: 'POST',
            body: JSON.stringify(config),
        });
    }

    async stopSimulation() {
        return this.request('/simulation/stop', {
            method: 'POST',
        });
    }

    async getSimulationStatus() {
        return this.request('/simulation/status');
    }

    async getSimulationData(limit = 50) {
        return this.request(`/simulation/data?limit=${limit}`);
    }

    // Profile endpoints
    async getProfiles() {
        return this.request('/profiles/');
    }

    async getProfileInfo(profileName) {
        return this.request(`/profiles/${profileName}`);
    }

    async generateProfilePreview(profileName, parameters) {
        return this.request(`/profiles/${profileName}/preview`, {
            method: 'POST',
            body: JSON.stringify(parameters),
        });
    }

    // MQTT endpoints
    async testMqttConnection(config) {
        return this.request('/mqtt/connect', {
            method: 'POST',
            body: JSON.stringify(config),
        });
    }

    async getMqttStatus() {
        return this.request('/mqtt/status');
    }

    // Health check
    async healthCheck() {
        return this.request('/health');
    }
}

// Export singleton instance
export const apiClient = new ApiClient(); 