<script>
	import { simulationActions } from '$lib/stores/simulation.js';

	export let mqttConfig;
	export let connectionStatus;

	async function testConnection() {
		try {
			await simulationActions.testConnection();
		} catch (error) {
			console.error('Connection test failed:', error);
		}
	}
</script>

<div class="space-y-4">
	<!-- Basic Connection Settings -->
	<div class="grid grid-cols-2 gap-4">
		<div>
			<label for="mqtt-host" class="block text-sm font-medium text-gray-700 mb-1">Host</label>
			<input 
				id="mqtt-host"
				type="text" 
				class="input-field"
				bind:value={$mqttConfig.host}
				placeholder="localhost"
			/>
		</div>
		<div>
			<label for="mqtt-port" class="block text-sm font-medium text-gray-700 mb-1">Port</label>
			<input 
				id="mqtt-port"
				type="number" 
				class="input-field"
				bind:value={$mqttConfig.port}
				min="1"
				max="65535"
			/>
		</div>
	</div>

	<div class="grid grid-cols-2 gap-4">
		<div>
			<label for="mqtt-username" class="block text-sm font-medium text-gray-700 mb-1">Username</label>
			<input 
				id="mqtt-username"
				type="text" 
				class="input-field"
				bind:value={$mqttConfig.username}
				placeholder="Optional"
			/>
		</div>
		<div>
			<label for="mqtt-password" class="block text-sm font-medium text-gray-700 mb-1">Password</label>
			<input 
				id="mqtt-password"
				type="password" 
				class="input-field"
				bind:value={$mqttConfig.password}
				placeholder="Optional"
			/>
		</div>
	</div>

	<!-- Advanced Settings -->
	<div class="border-t pt-4">
		<h4 class="text-sm font-medium text-gray-700 mb-3">Advanced Settings</h4>
		
		<div class="grid grid-cols-2 gap-4">
			<div>
				<label for="mqtt-keepalive" class="block text-sm font-medium text-gray-700 mb-1">Keepalive (s)</label>
				<input 
					id="mqtt-keepalive"
					type="number" 
					class="input-field"
					bind:value={$mqttConfig.keepalive}
					min="1"
				/>
			</div>
			<div>
				<label for="mqtt-qos" class="block text-sm font-medium text-gray-700 mb-1">QoS</label>
				<select id="mqtt-qos" class="input-field" bind:value={$mqttConfig.qos}>
					<option value={0}>0 - At most once</option>
					<option value={1}>1 - At least once</option>
					<option value={2}>2 - Exactly once</option>
				</select>
			</div>
		</div>

		<div class="grid grid-cols-2 gap-4 mt-4">
			<div class="flex items-center">
				<input 
					id="mqtt-clean-session"
					type="checkbox" 
					class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
					bind:checked={$mqttConfig.cleanSession}
				/>
				<label for="mqtt-clean-session" class="ml-2 block text-sm text-gray-700">
					Clean Session
				</label>
			</div>
			<div class="flex items-center">
				<input 
					id="mqtt-retained"
					type="checkbox" 
					class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
					bind:checked={$mqttConfig.retained}
				/>
				<label for="mqtt-retained" class="ml-2 block text-sm text-gray-700">
					Retained Messages
				</label>
			</div>
		</div>

		<!-- Last Will and Testament -->
		<div class="mt-4 space-y-3">
			<h5 class="text-sm font-medium text-gray-700">Last Will & Testament</h5>
			<div class="grid grid-cols-2 gap-4">
				<div>
					<label for="mqtt-lwt-topic" class="block text-sm font-medium text-gray-700 mb-1">Topic</label>
					<input 
						id="mqtt-lwt-topic"
						type="text" 
						class="input-field"
						bind:value={$mqttConfig.lastWillTopic}
						placeholder="Optional"
					/>
				</div>
				<div>
					<label for="mqtt-lwt-qos" class="block text-sm font-medium text-gray-700 mb-1">QoS</label>
					<select id="mqtt-lwt-qos" class="input-field" bind:value={$mqttConfig.lastWillQos}>
						<option value={0}>0 - At most once</option>
						<option value={1}>1 - At least once</option>
						<option value={2}>2 - Exactly once</option>
					</select>
				</div>
			</div>
			<div>
				<label for="mqtt-lwt-message" class="block text-sm font-medium text-gray-700 mb-1">Message</label>
				<input 
					id="mqtt-lwt-message"
					type="text" 
					class="input-field"
					bind:value={$mqttConfig.lastWillMessage}
					placeholder="Optional"
				/>
			</div>
		</div>
	</div>

	<!-- Connection Test -->
	<div class="border-t pt-4">
		<div class="flex items-center justify-between">
			<div>
				<button 
					type="button"
					class="btn-primary"
					on:click={testConnection}
					disabled={$connectionStatus.isTesting}
				>
					{#if $connectionStatus.isTesting}
						Testing...
					{:else}
						Test Connection
					{/if}
				</button>
			</div>
			<div class="flex items-center space-x-2">
				<span class="text-sm text-gray-600">Status:</span>
				{#if $connectionStatus.isConnected}
					<span class="status-connected">Connected</span>
				{:else if $connectionStatus.error}
					<span class="status-disconnected">Failed</span>
				{:else}
					<span class="text-gray-400">Not tested</span>
				{/if}
			</div>
		</div>
		
		{#if $connectionStatus.error}
			<div class="mt-2 text-sm text-red-600">
				{$connectionStatus.error}
			</div>
		{/if}
	</div>
</div> 