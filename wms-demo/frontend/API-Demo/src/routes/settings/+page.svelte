<script>
  import { writable } from "svelte/store";
  import { setIpConfig, getPoints, updatePointName } from "$lib/api";
  import { onMount } from "svelte";
  // import { debounce } from "lodash"; // If using debounce

  let ip = writable("127.0.0.1");
  let port = writable("8000");
  let feedbackMessage = writable("");
  let feedbackType = writable("");

  let points = [];

  onMount(async () => {
    try {
      points = await getPoints();
    } catch (error) {
      console.error('Error fetching points:', error);
    }
  });

  async function updateIP() {
    const payload = { ip: $ip, port: $port };

    try {
      const response = await setIpConfig(payload);
      feedbackMessage.set(response.message);
      feedbackType.set("success");
    } catch (error) {
      feedbackMessage.set("An error occurred while updating IP and Port.");
      feedbackType.set("error");
    }
  }

  // If using debounce
  // const debouncedSavePointName = debounce(async (point) => {
  //   try {
  //     await updatePointName(point.name, point.wms_name);
  //     feedbackMessage.set(`Point ${point.name} updated successfully.`);
  //     feedbackType.set("success");
  //   } catch (error) {
  //     feedbackMessage.set(`Failed to update point ${point.name}.`);
  //     feedbackType.set("error");
  //   }
  // }, 500);

  async function savePointName(point) {
    // If using debounce
    // debouncedSavePointName(point);

    // Without debounce
    try {
      await updatePointName(point.name, point.wms_name);
      feedbackMessage.set(`Point ${point.name} updated successfully.`);
      feedbackType.set("success");
    } catch (error) {
      feedbackMessage.set(`Failed to update point ${point.name}.`);
      feedbackType.set("error");
    }
  }
</script>

<div class="container mx-auto p-8">
  <h1 class="text-3xl font-bold mb-6">Settings</h1>

  <div class="card p-4">
    <h2 class="text-xl font-bold mb-4">Set KUKA AMR-Fleet's standard API's IP address and Port number</h2>

    <form on:submit|preventDefault={updateIP} class="space-y-4">
      <div>
        <label for="ip" class="block font-medium">IP Address:</label>
        <input id="ip" type="text" bind:value={$ip} class="w-full border p-2 rounded" />
      </div>

      <div>
        <label for="port" class="block font-medium">Port:</label>
        <input id="port" type="text" bind:value={$port} class="w-full border p-2 rounded" />
      </div>

      <button type="submit" class="bg-blue-600 text-white font-semibold py-2 px-6 rounded hover:bg-blue-700 transition duration-200">
        Update Settings
      </button>
    </form>
  </div>

  {#if $feedbackMessage}
    <div class="mt-4 p-4 rounded { $feedbackType === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800' }">
      {$feedbackMessage}
    </div>
  {/if}

  <!-- Points Mapping Section -->
  <div class="card p-4 mt-8">
    <h2 class="text-xl font-bold mb-4">Point Name Mapping</h2>
    <dl class="list-dl">
      {#each points as point}
        <div class="flex items-center mb-2">
          <span class="badge bg-primary-500 mr-4">📍</span>
          <span class="flex-auto">
            <dt>{point.name}</dt>
            <dd>
              <input
                type="text"
                bind:value={point.wms_name}
                on:change={() => savePointName(point)}
                class="border p-1 rounded w-full"
              />
            </dd>
          </span>
        </div>
      {/each}
    </dl>
  </div>
</div>

<style>
  /* Existing styles */

  .bg-green-100 {
    background-color: #f0fff4;
  }
  .text-green-800 {
    color: #22543d;
  }
  .bg-red-100 {
    background-color: #fff5f5;
  }
  .text-red-800 {
    color: #c53030;
  }

  /* Additional styles for the badge and list */
  .badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background-color: #4299e1;
    color: white;
    font-size: 16px;
  }
  .list-dl div {
    display: flex;
    align-items: center;
  }
  dt {
    font-weight: bold;
  }
  dd {
    margin-left: 0;
  }
</style>
