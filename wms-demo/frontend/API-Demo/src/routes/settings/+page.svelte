<script>
  import { writable } from "svelte/store";
  import { setIpConfig, getPoints, updatePointName, addPoint } from "$lib/api";
  import { onMount } from "svelte";
  // import { debounce } from "lodash"; // If using debounce

  let ip = writable("127.0.0.1");
  let port = writable("8000");
  let feedbackMessage = writable("");
  let feedbackType = writable("");

  let points = [];
  let newPoint = {
    name: "",
    position: "",
    wms_name: ""
  };

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

  async function handleAddPoint() {
    if (!newPoint.name || !newPoint.position) {
      feedbackMessage.set("Point name and position are required.");
      feedbackType.set("error");
      return;
    }

    try {
      await addPoint({
        name: newPoint.name,
        position: newPoint.position,
        wms_name: newPoint.wms_name || newPoint.name
      });
      feedbackMessage.set(`Point ${newPoint.name} added successfully.`);
      feedbackType.set("success");
      newPoint = { name: "", position: "", wms_name: "" };
      points = await getPoints();
    } catch (error) {
      feedbackMessage.set(error?.message || "Failed to add point.");
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
    {#if points.length === 0}
      <p class="text-gray-600 mb-4">
        No points available. Connect to Fleet Manager or add points manually below.
      </p>
    {/if}
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

    <!-- Manual Add Point Section -->
    <div class="mt-6 border-t pt-4">
      <h3 class="text-lg font-bold mb-2">Add Point Manually</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label for="new-point-name" class="block font-medium">Point Name:</label>
          <input id="new-point-name" type="text" bind:value={newPoint.name} class="w-full border p-2 rounded" />
        </div>
        <div>
          <label for="new-point-position" class="block font-medium">Position:</label>
          <input id="new-point-position" type="text" bind:value={newPoint.position} class="w-full border p-2 rounded" />
        </div>
        <div>
          <label for="new-point-wms" class="block font-medium">WMS Name (optional):</label>
          <input id="new-point-wms" type="text" bind:value={newPoint.wms_name} class="w-full border p-2 rounded" />
        </div>
      </div>
      <button
        type="button"
        on:click={handleAddPoint}
        class="mt-4 bg-blue-600 text-white font-semibold py-2 px-6 rounded hover:bg-blue-700 transition duration-200"
      >
        Add Point
      </button>
    </div>
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
