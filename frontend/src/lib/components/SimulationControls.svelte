<script>
	import { simulationActions } from '$lib/stores/simulation.js';

	export let simulationConfig;
	export let simulationStatus;
	export let selectedProfile;
	export let connectionStatus;

	let starting = false;
	let stopping = false;
	let error = null;

	async function startSimulation() {
		if (!$selectedProfile) {
			error = 'Please select a profile first';
			return;
		}

		if (!$connectionStatus.isConnected) {
			error = 'Please test MQTT connection first';
			return;
		}

		starting = true;
		error = null;

		try {
			await simulationActions.startSimulation();
		} catch (err) {
			error = err.message;
		} finally {
			starting = false;
		}
	}

	async function stopSimulation() {
		stopping = true;
		error = null;

		try {
			await simulationActions.stopSimulation();
		} catch (err) {
			error = err.message;
		} finally {
			stopping = false;
		}
	}
</script>

<div class="space-y-4">
	<!-- Simulation Settings -->
	<div class="grid grid-cols-2 gap-4">
		<div>
			<label for="sim-interval" class="block text-sm font-medium text-gray-700 mb-1">Interval (seconds)</label>
			<input 
				id="sim-interval"
				type="number" 
				class="input-field"
				bind:value={$simulationConfig.interval}
				min="1"
				max="3600"
			/>
		</div>
		<div>
			<label for="sim-duration" class="block text-sm font-medium text-gray-700 mb-1">Duration (seconds)</label>
			<input 
				id="sim-duration"
				type="number" 
				class="input-field"
				bind:value={$simulationConfig.duration}
				min="1"
				placeholder="Infinite"
			/>
		</div>
	</div>

	<!-- Control Buttons -->
	<div class="space-y-3">
		{#if $simulationStatus.isRunning}
			<button 
				type="button"
				class="btn-danger w-full"
				on:click={stopSimulation}
				disabled={stopping}
			>
				{#if stopping}
					Stopping...
				{:else}
					Stop Simulation
				{/if}
			</button>
		{:else}
			<button 
				type="button"
				class="btn-primary w-full"
				on:click={startSimulation}
				disabled={starting || !$selectedProfile || !$connectionStatus.isConnected}
			>
				{#if starting}
					Starting...
				{:else}
					Start Simulation
				{/if}
			</button>
		{/if}
	</div>

	<!-- Error Display -->
	{#if error}
		<div class="bg-red-100 border border-red-400 text-red-700 px-3 py-2 rounded text-sm">
			{error}
		</div>
	{/if}

	<!-- Status Summary -->
	<div class="border-t pt-4">
		<div class="space-y-2 text-sm">
			<div class="flex justify-between">
				<span class="text-gray-600">Profile:</span>
				<span class="font-medium">{$selectedProfile?.name || 'None'}</span>
			</div>
			<div class="flex justify-between">
				<span class="text-gray-600">Status:</span>
				{#if $simulationStatus.isRunning}
					<span class="status-running">Running</span>
				{:else}
					<span class="text-gray-400">Stopped</span>
				{/if}
			</div>
			<div class="flex justify-between">
				<span class="text-gray-600">Messages Sent:</span>
				<span class="font-medium">{$simulationStatus.messagesSent}</span>
			</div>
			{#if $simulationStatus.startTime}
				<div class="flex justify-between">
					<span class="text-gray-600">Started:</span>
					<span class="font-medium">{new Date($simulationStatus.startTime).toLocaleTimeString()}</span>
				</div>
			{/if}
		</div>
	</div>
</div> 