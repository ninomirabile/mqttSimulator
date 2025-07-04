/**
 * Simulation Store
 * Manages the state of MQTT simulation
 */

import { writable } from 'svelte/store';
import { apiClient } from '../api.js';

// Create stores
export const simulationStatus = writable({
    isRunning: false,
    isConnected: false,
    profileName: null,
    topic: null,
    interval: null,
    messagesSent: 0,
    startTime: null,
    lastMessage: null
});

export const simulationData = writable({
    messages: [],
    totalCount: 0
});

export const profiles = writable([]);
export const selectedProfile = writable(null);
export const profilePreview = writable(null);
export const profileParams = writable({});

export const mqttConfig = writable({
    host: 'test.mosquitto.org',
    port: 1883,
    username: '',
    password: '',
    keepalive: 60,
    cleanSession: true,
    qos: 1,
    retained: false,
    lastWillTopic: '',
    lastWillMessage: '',
    lastWillQos: 0
});

export const simulationConfig = writable({
    interval: 5,
    duration: null
});

export const connectionStatus = writable({
    isConnected: false,
    isTesting: false,
    error: null
});

// Actions
export const simulationActions = {
    async loadProfiles() {
        try {
            const response = await apiClient.getProfiles();
            profiles.set(response.profiles);
        } catch (error) {
            console.error('Failed to load profiles:', error);
            throw error;
        }
    },

    async selectProfile(profileName) {
        try {
            const response = await apiClient.getProfileInfo(profileName);
            selectedProfile.set(response);
            profileParams.set({ ...response.parameters });
            
            // Generate preview with default parameters
            const previewResponse = await apiClient.generateProfilePreview(profileName, {});
            profilePreview.set(previewResponse.data.preview);
        } catch (error) {
            console.error('Failed to select profile:', error);
            throw error;
        }
    },

    async generatePreview(profileName, parameters) {
        try {
            const response = await apiClient.generateProfilePreview(profileName, parameters);
            profilePreview.set(response.data.preview);
        } catch (error) {
            console.error('Failed to generate preview:', error);
            throw error;
        }
    },

    async testConnection() {
        connectionStatus.update(status => ({ ...status, isTesting: true, error: null }));
        try {
            const config = get(mqttConfig);
            // Conversione camelCase -> snake_case per compatibilità backend
            const apiConfig = {
                host: config.host,
                port: config.port,
                username: config.username,
                password: config.password,
                keepalive: config.keepalive,
                clean_session: config.cleanSession,
                qos: config.qos,
                retained: config.retained,
                last_will_topic: config.lastWillTopic || null,
                last_will_message: config.lastWillMessage || null,
                last_will_qos: config.lastWillQos || 0
            };
            const response = await apiClient.testMqttConnection(apiConfig);
            console.log("MQTT test response:", response);
            connectionStatus.update(status => ({
                ...status,
                isTesting: false,
                isConnected: response.success,
                error: response.success ? null : response.message
            }));
            return response.success;
        } catch (error) {
            connectionStatus.update(status => ({
                ...status,
                isTesting: false,
                isConnected: false,
                error: error.message
            }));
            throw error;
        }
    },

    async startSimulation() {
        try {
            const mqtt = get(mqttConfig);
            const sim = get(simulationConfig);
            const profile = get(selectedProfile);
            
            if (!profile) {
                throw new Error('No profile selected');
            }

            const config = {
                mqtt,
                profile: {
                    name: profile.name,
                    parameters: profile.parameters || {},
                    topic: null // Use default topic
                },
                interval: sim.interval,
                duration: sim.duration
            };

            const response = await apiClient.startSimulation(config);
            
            if (response.success) {
                // Update status
                await this.updateStatus();
            }
            
            return response;
        } catch (error) {
            console.error('Failed to start simulation:', error);
            throw error;
        }
    },

    async stopSimulation() {
        try {
            const response = await apiClient.stopSimulation();
            
            if (response.success) {
                // Update status
                await this.updateStatus();
            }
            
            return response;
        } catch (error) {
            console.error('Failed to stop simulation:', error);
            throw error;
        }
    },

    async updateStatus() {
        try {
            const status = await apiClient.getSimulationStatus();
            simulationStatus.set({
                isRunning: status.is_running,
                isConnected: status.is_connected,
                profileName: status.profile_name,
                topic: status.topic,
                interval: status.interval,
                messagesSent: status.messages_sent,
                startTime: status.start_time,
                lastMessage: status.last_message
            });
        } catch (error) {
            console.error('Failed to update status:', error);
        }
    },

    async loadSimulationData(limit = 50) {
        try {
            const data = await apiClient.getSimulationData(limit);
            simulationData.set({
                messages: data.messages,
                totalCount: data.total_count
            });
        } catch (error) {
            console.error('Failed to load simulation data:', error);
        }
    }
};

// Helper function to get store value
function get(store) {
    let value;
    store.subscribe(v => value = v)();
    return value;
}

// Auto-update status when simulation is running
let statusInterval;

simulationStatus.subscribe(status => {
    if (status.isRunning) {
        if (!statusInterval) {
            statusInterval = setInterval(() => {
                simulationActions.updateStatus();
                simulationActions.loadSimulationData();
            }, 1000);
        }
    } else {
        if (statusInterval) {
            clearInterval(statusInterval);
            statusInterval = null;
        }
    }
}); 