<script context="module" lang="ts">
	// Tipi generici per i profili
	export interface ProfileInfo {
		name: string;
		description: string;
		parameters: Record<string, any>;
		example_topic: string;
		example_payload: Record<string, any>;
	}
</script>
<script lang="ts">
	import { simulationActions, profileParams } from '$lib/stores/simulation.js';
	import { createEventDispatcher } from 'svelte';
	import { onMount } from 'svelte';
	import { get } from 'svelte/store';

	export let profiles: ProfileInfo[] = [];
	export let selectedProfile: ProfileInfo | null = null;
	export let profilePreview: Record<string, any> | null = null;

	const dispatch = createEventDispatcher();

	let params: Record<string, any> = {};

	onMount(() => {
		params = get(profileParams);
	});

	$: params = get(profileParams);

	async function handleProfileSelect(event: Event) {
		const target = event.target as HTMLSelectElement | null;
		const profileName = target ? target.value : '';
		if (profileName) {
			try {
				await simulationActions.selectProfile(profileName);
				dispatch('profileSelected', { profileName });
			} catch (error) {
				console.error('Failed to select profile:', error);
			}
		}
	}

	// Aggiorna la preview ogni volta che cambiano i parametri
	$: if (selectedProfile && Object.keys(params).length > 0) {
		simulationActions.generatePreview(selectedProfile.name, params);
	}

	function handleParamChange(key: string, event: Event) {
		const target = event.target as HTMLInputElement | null;
		const value = target ? target.value : '';
		const updated = { ...params, [key]: typeof params[key] === 'number' ? +value : value };
		profileParams.set(updated);
	}

	function formatJson(obj: any) {
		return JSON.stringify(obj, null, 2);
	}
</script>

<div class="space-y-4">
	<!-- Profile Dropdown -->
	<div>
		<label for="profile-select" class="block text-sm font-medium text-gray-700 mb-2">
			Select Profile
		</label>
		<select 
			id="profile-select"
			class="input-field"
			on:change={handleProfileSelect}
			value={selectedProfile?.name || ''}
		>
			<option value="">Choose a profile...</option>
			{#each profiles as profile}
				<option value={profile.name}>{profile.name}</option>
			{/each}
		</select>
	</div>

	<!-- Profile Information & Dynamic Form -->
	{#if selectedProfile}
		<div class="space-y-3">
			<div>
				<h3 class="text-lg font-medium text-gray-900">{selectedProfile.name}</h3>
				<p class="text-sm text-gray-600">{selectedProfile.description}</p>
			</div>

			<!-- Example Topic -->
			<div>
				<label class="block text-sm font-medium text-gray-700 mb-1">Example Topic</label>
				<code class="block bg-gray-100 px-3 py-2 rounded text-sm font-mono">
					{selectedProfile.example_topic}
				</code>
			</div>

			<!-- Dynamic Parameters Form -->
			{#if Object.keys(selectedProfile.parameters || {}).length > 0}
				<div>
					<label class="block text-sm font-medium text-gray-700 mb-1">Parameters</label>
					<form class="space-y-2">
						{#each Object.entries(selectedProfile.parameters) as [key, value]}
							<div class="flex items-center space-x-2">
								<label class="w-32 text-sm text-gray-700">{key}</label>
								{#if typeof value === 'number'}
									<input
										type="number"
										class="input-field flex-1"
										bind:value={params[key]}
										on:input={e => handleParamChange(key, e)}
									/>
								{:else}
									<input
										type="text"
										class="input-field flex-1"
										bind:value={params[key]}
										on:input={e => handleParamChange(key, e)}
									/>
								{/if}
							</div>
						{/each}
					</form>
				</div>
			{/if}

			<!-- Preview -->
			{#if profilePreview}
				<div>
					<label class="block text-sm font-medium text-gray-700 mb-1">Data Preview</label>
					<pre class="bg-gray-100 p-3 rounded text-xs overflow-auto max-h-32">{formatJson(profilePreview)}</pre>
				</div>
			{/if}
		</div>
	{:else}
		<div class="text-center py-8 text-gray-500">
			<p>Select a profile to see details and preview</p>
		</div>
	{/if}
</div> 