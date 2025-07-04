<script>
	export let simulationStatus;

	function formatDuration(startTime) {
		if (!startTime) return '0s';
		
		const start = new Date(startTime);
		const now = new Date();
		const diff = Math.floor((now - start) / 1000);
		
		if (diff < 60) return `${diff}s`;
		if (diff < 3600) return `${Math.floor(diff / 60)}m ${diff % 60}s`;
		return `${Math.floor(diff / 3600)}h ${Math.floor((diff % 3600) / 60)}m`;
	}

	function formatJson(obj) {
		return JSON.stringify(obj, null, 2);
	}
</script>

<div class="space-y-4">
	<!-- Status Cards -->
	<div class="grid grid-cols-2 gap-4">
		<div class="bg-gray-50 p-4 rounded-lg">
			<div class="flex items-center justify-between">
				<span class="text-sm font-medium text-gray-600">Connection</span>
				{#if $simulationStatus.isConnected}
					<span class="status-connected">Connected</span>
				{:else}
					<span class="status-disconnected">Disconnected</span>
				{/if}
			</div>
		</div>
		
		<div class="bg-gray-50 p-4 rounded-lg">
			<div class="flex items-center justify-between">
				<span class="text-sm font-medium text-gray-600">Simulation</span>
				{#if $simulationStatus.isRunning}
					<span class="status-running">Running</span>
				{:else}
					<span class="text-gray-400">Stopped</span>
				{/if}
			</div>
		</div>
	</div>

	<!-- Details -->
	<div class="space-y-3">
		{#if $simulationStatus.profileName}
			<div class="flex justify-between items-center py-2 border-b border-gray-200">
				<span class="text-sm font-medium text-gray-600">Profile</span>
				<span class="text-sm text-gray-900">{$simulationStatus.profileName}</span>
			</div>
		{/if}

		{#if $simulationStatus.topic}
			<div class="flex justify-between items-center py-2 border-b border-gray-200">
				<span class="text-sm font-medium text-gray-600">Topic</span>
				<code class="text-sm bg-gray-100 px-2 py-1 rounded font-mono">{$simulationStatus.topic}</code>
			</div>
		{/if}

		{#if $simulationStatus.interval}
			<div class="flex justify-between items-center py-2 border-b border-gray-200">
				<span class="text-sm font-medium text-gray-600">Interval</span>
				<span class="text-sm text-gray-900">{$simulationStatus.interval}s</span>
			</div>
		{/if}

		<div class="flex justify-between items-center py-2 border-b border-gray-200">
			<span class="text-sm font-medium text-gray-600">Messages Sent</span>
			<span class="text-sm text-gray-900">{$simulationStatus.messagesSent}</span>
		</div>

		{#if $simulationStatus.startTime}
			<div class="flex justify-between items-center py-2 border-b border-gray-200">
				<span class="text-sm font-medium text-gray-600">Started</span>
				<span class="text-sm text-gray-900">{new Date($simulationStatus.startTime).toLocaleString()}</span>
			</div>

			<div class="flex justify-between items-center py-2 border-b border-gray-200">
				<span class="text-sm font-medium text-gray-600">Duration</span>
				<span class="text-sm text-gray-900">{formatDuration($simulationStatus.startTime)}</span>
			</div>
		{/if}
	</div>

	<!-- Last Message -->
	{#if $simulationStatus.lastMessage}
		<div class="border-t pt-4">
			<h4 class="text-sm font-medium text-gray-700 mb-2">Last Message</h4>
			<pre class="bg-gray-100 p-3 rounded text-xs overflow-auto max-h-32 font-mono">{formatJson($simulationStatus.lastMessage)}</pre>
		</div>
	{/if}

	<!-- Empty State -->
	{#if !$simulationStatus.isRunning && !$simulationStatus.isConnected}
		<div class="text-center py-8 text-gray-500">
			<div class="text-4xl mb-2">📡</div>
			<p class="text-sm">No active simulation</p>
			<p class="text-xs">Configure MQTT settings and start a simulation</p>
		</div>
	{/if}
</div> 