<script lang="ts">
import { selectedProfile, profileParams, mqttConfig, simulationConfig } from '$lib/stores/simulation.js';
import { get } from 'svelte/store';

function formatJson(obj: any) {
	return JSON.stringify(obj, null, 2);
}

const profile = get(selectedProfile) as { name?: string } | null;
</script>

<div class="card bg-blue-50 border-blue-200">
	<h2 class="text-lg font-semibold mb-2 text-blue-900">Configuration Summary</h2>
	<div class="space-y-2 text-sm">
		<!-- Profilo -->
		<div class="flex justify-between">
			<span class="font-medium text-blue-800">Profile:</span>
			<span>{profile?.name ?? 'None'}</span>
		</div>
		<!-- Parametri profilo -->
		{#if profile}
			<div>
				<span class="font-medium text-blue-800">Profile Parameters:</span>
				<pre class="bg-blue-100 rounded p-2 mt-1 text-xs overflow-auto max-h-32">{formatJson(get(profileParams))}</pre>
			</div>
		{/if}
		<!-- MQTT Config -->
		<div>
			<span class="font-medium text-blue-800">MQTT Config:</span>
			<pre class="bg-blue-100 rounded p-2 mt-1 text-xs overflow-auto max-h-32">{formatJson(get(mqttConfig))}</pre>
		</div>
		<!-- Simulazione -->
		<div>
			<span class="font-medium text-blue-800">Simulation:</span>
			<pre class="bg-blue-100 rounded p-2 mt-1 text-xs overflow-auto max-h-32">{formatJson(get(simulationConfig))}</pre>
		</div>
	</div>
</div> 