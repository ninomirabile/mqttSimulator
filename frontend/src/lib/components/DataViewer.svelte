<script>
	import { onMount } from 'svelte';
	import { simulationActions } from '$lib/stores/simulation.js';

	export let simulationData;
	export let simulationStatus;

	let autoScroll = true;
	let maxMessages = 50;

	onMount(() => {
		// Auto-scroll to bottom when new messages arrive
		const unsubscribe = simulationData.subscribe(data => {
			if (autoScroll && data.messages.length > 0) {
				setTimeout(() => {
					const container = document.getElementById('messages-container');
					if (container) {
						container.scrollTop = container.scrollHeight;
					}
				}, 100);
			}
		});

		return unsubscribe;
	});

	function formatTimestamp(timestamp) {
		return new Date(timestamp).toLocaleTimeString();
	}

	function formatJson(obj) {
		return JSON.stringify(obj, null, 2);
	}

	function clearMessages() {
		simulationData.set({ messages: [], totalCount: $simulationData.totalCount });
	}

	function toggleAutoScroll() {
		autoScroll = !autoScroll;
	}
</script>

<div class="space-y-4">
	<!-- Header -->
	<div class="flex items-center justify-between">
		<div class="flex items-center space-x-4">
			<h3 class="text-lg font-medium text-gray-900">Live Data Stream</h3>
			<span class="text-sm text-gray-500">({$simulationData.messages.length} recent, {$simulationData.totalCount} total)</span>
		</div>
		
		<div class="flex items-center space-x-2">
			<label class="flex items-center text-sm">
				<input 
					type="checkbox" 
					bind:checked={autoScroll}
					class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
				/>
				<span class="ml-2">Auto-scroll</span>
			</label>
			
			<button 
				type="button"
				class="btn-secondary text-sm"
				on:click={clearMessages}
			>
				Clear
			</button>
		</div>
	</div>

	<!-- Messages Container -->
	<div 
		id="messages-container"
		class="bg-gray-50 border border-gray-200 rounded-lg p-4 h-96 overflow-y-auto space-y-3"
	>
		{#if $simulationData.messages.length === 0}
			<div class="text-center py-8 text-gray-500">
				<div class="text-4xl mb-2">📊</div>
				<p class="text-sm">No messages yet</p>
				<p class="text-xs">Start a simulation to see live data</p>
			</div>
		{:else}
			{#each $simulationData.messages.slice(-maxMessages) as message, index}
				<div class="bg-white border border-gray-200 rounded-lg p-3">
					<div class="flex items-center justify-between mb-2">
						<div class="flex items-center space-x-2">
							<span class="text-xs font-medium text-gray-500">#{index + 1}</span>
							<code class="text-xs bg-gray-100 px-2 py-1 rounded font-mono">{message.topic}</code>
						</div>
						<span class="text-xs text-gray-500">{formatTimestamp(message.timestamp)}</span>
					</div>
					
					<pre class="text-xs bg-gray-50 p-2 rounded overflow-auto max-h-32 font-mono">{formatJson(message.payload)}</pre>
				</div>
			{/each}
		{/if}
	</div>

	<!-- Footer -->
	<div class="flex items-center justify-between text-sm text-gray-600">
		<div>
			Showing last {Math.min($simulationData.messages.length, maxMessages)} messages
		</div>
		
		{#if $simulationStatus.isRunning}
			<div class="flex items-center space-x-2">
				<div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
				<span>Live</span>
			</div>
		{/if}
	</div>
</div> 