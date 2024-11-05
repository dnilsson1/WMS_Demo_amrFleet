<script>
    import { writable } from "svelte/store";
    import { createContainer, addProductToContainer } from "$lib/api";
    import { ContainerType, EmptyStatus } from "$lib/constants";
    
    let containers = [];
    let newContainer = {
      containerCode: "",
      containerType: "RACK",
      position: "",
      emptyStatus: "EMPTY",
      contents: {}
    };
  
    async function handleCreateContainer() {
      await createContainer(newContainer);
      // Reset form and reload containers
      newContainer = {
        containerCode: "",
        containerType: "RACK",
        position: "",
        emptyStatus: "EMPTY",
        contents: {}
      };
    }
  </script>
  
  <div class="space-y-8">
    <div class="card p-4">
      <h2 class="text-xl font-bold mb-4">Add New Container</h2>
      <form on:submit|preventDefault={handleCreateContainer} class="space-y-4">
        <div>
          <label for="container-code" class="block">Container Code:</label>
          <input id="container-code" type="text" bind:value={newContainer.containerCode} class="w-full border p-2 rounded" />
        </div>
        <div>
          <label for="container-type" class="block">Type:</label>
          <select id="container-type" bind:value={newContainer.containerType} class="w-full border p-2 rounded">
            <option value="RACK">Rack</option>
            <option value="BIN">Bin</option>
            <option value="BUCKET">Bucket</option>
          </select>
        </div>
        <div>
          <label for="container-position" class="block">Position:</label>
          <input id="container-position" type="text" bind:value={newContainer.position} class="w-full border p-2 rounded" />
        </div>
        <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">
          Create Container
        </button>
      </form>
    </div>
  </div>
  