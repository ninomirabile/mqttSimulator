<script>
	import '../app.css';
	import { onMount } from 'svelte';
	import { simulationActions } from '$lib/stores/simulation.js';

	onMount(async () => {
		// Load profiles on app start
		try {
			await simulationActions.loadProfiles();
		} catch (error) {
			console.error('Failed to load profiles on startup:', error);
		}
	});
</script>

<main class="min-h-screen bg-gray-50">
	<slot />
</main> 