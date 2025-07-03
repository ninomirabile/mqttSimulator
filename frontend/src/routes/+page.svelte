<script lang="ts">
	import { onMount } from 'svelte';
	import { 
		simulationStatus, 
		simulationData, 
		profiles, 
		selectedProfile, 
		profilePreview,
		mqttConfig,
		simulationConfig,
		connectionStatus,
		simulationActions 
	} from '$lib/stores/simulation.js';
	
	import ProfileSelector from '$lib/components/ProfileSelector.svelte';
	import MqttConfig from '$lib/components/MqttConfig.svelte';
	import SimulationControls from '$lib/components/SimulationControls.svelte';
	import StatusDisplay from '$lib/components/StatusDisplay.svelte';
	import DataViewer from '$lib/components/DataViewer.svelte';
	import ConfigSummary from '$lib/components/ConfigSummary.svelte';

	let loading = true;
	let error: string | null = null;

	onMount(async () => {
		try {
			await simulationActions.updateStatus();
			await simulationActions.loadSimulationData();
		} catch (err) {
			error = (err as Error).message;
		} finally {
			loading = false;
		}
	});
</script>

<svelte:head>
	<title>MQTT Simulator Dashboard</title>
</svelte:head>

<div class="container mx-auto px-4 py-8">
	<!-- Header -->
	<header class="mb-8">
		<h1 class="text-4xl font-bold text-gray-900 mb-2">MQTT Simulator</h1>
		<p class="text-gray-600">Real-time data simulation with configurable profiles</p>
	</header>

	{#if loading}
		<div class="flex justify-center items-center h-64">
			<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
		</div>
	{:else if error}
		<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
			<strong>Error:</strong> {error}
		</div>
	{:else}
		<div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
			<!-- Left Column - Configuration -->
			<div class="lg:col-span-1 space-y-6">
				<!-- Config Summary -->
				<ConfigSummary />
				<!-- Profile Selection -->
				<div class="card">
					<h2 class="text-xl font-semibold mb-4">Profile Selection</h2>
					<ProfileSelector profiles={$profiles} selectedProfile={$selectedProfile} profilePreview={$profilePreview} />
				</div>

				<!-- MQTT Configuration -->
				<div class="card">
					<h2 class="text-xl font-semibold mb-4">MQTT Configuration</h2>
					<MqttConfig {mqttConfig} {connectionStatus} />
				</div>

				<!-- Simulation Controls -->
				<div class="card">
					<h2 class="text-xl font-semibold mb-4">Simulation Controls</h2>
					<SimulationControls 
						{simulationConfig} 
						{simulationStatus} 
						{selectedProfile}
						{connectionStatus}
					/>
				</div>
			</div>

			<!-- Right Column - Status and Data -->
			<div class="lg:col-span-2 space-y-6">
				<!-- Status Display -->
				<div class="card">
					<h2 class="text-xl font-semibold mb-4">Simulation Status</h2>
					<StatusDisplay {simulationStatus} />
				</div>

				<!-- Data Viewer -->
				<div class="card">
					<h2 class="text-xl font-semibold mb-4">Live Data Stream</h2>
					<DataViewer {simulationData} {simulationStatus} />
				</div>
			</div>
		</div>
	{/if}
</div> 