<script>
  import { writable } from "svelte/store";
  import { createContainer, createContainerAndEnter, getProducts, getContainers } from "$lib/api";
  import { ContainerType, EmptyStatus } from "$lib/constants";
  import { onMount } from "svelte";

  let containers = [];
  let products = [];
  let newContainer = {
    containerCode: "",
    containerType: "RACK",
    position: "",
    emptyStatus: "EMPTY",
    containerModelCode: "",
    enterOrientation: "",
    isNew: false,
    contents: [],
  };

  onMount(async () => {
    try {
      products = await getProducts();
      containers = await getContainers();
    } catch (error) {
      console.error("Error initializing data:", error);
    }
  });

  function addProduct() {
    newContainer.contents = [...newContainer.contents, { product_id: "", quantity: 1 }];
  }

  function removeProduct(index) {
    newContainer.contents = newContainer.contents.filter((_, i) => i !== index);
  }

  async function handleCreateContainer() {
    try {
      const containerCode = (newContainer.containerCode || "").trim();
      const position = (newContainer.position || "").trim();

      if (!containerCode || !position) {
        alert("Container code and position are required.");
        return;
      }

      const containerData = {
        containerCode,
        containerType: newContainer.containerType,
        position,
        emptyStatus: newContainer.emptyStatus,
        contents: Object.fromEntries(newContainer.contents.map((item) => [item.product_id, item.quantity])),
      };

      console.log("Payload being sent to Create:", containerData);

      await createContainer(containerData);

      newContainer = {
        containerCode: "",
        containerType: "RACK",
        position: "",
        emptyStatus: "EMPTY",
        containerModelCode: "",
        enterOrientation: "",
        isNew: false,
        contents: [],
      };

      alert("Container created locally.");
    } catch (error) {
      console.error("Error creating container:", error);
      alert("Failed to create container.");
    }
  }

  async function handleCreateAndEnterContainer() {
    try {
      const containerCode = (newContainer.containerCode || "").trim();
      const position = (newContainer.position || "").trim();

      if (!containerCode || !position) {
        alert("Container code and position are required.");
        return;
      }

      const containerData = {
        containerCode,
        containerType: newContainer.containerType,
        position,
        containerModelCode: newContainer.containerModelCode,
        enterOrientation: newContainer.enterOrientation,
        isNew: newContainer.isNew,
      };

      console.log("Payload being sent to Create & Enter:", containerData);

      await createContainerAndEnter(containerData);

      newContainer = {
        containerCode: "",
        containerType: "RACK",
        position: "",
        emptyStatus: "EMPTY",
        containerModelCode: "",
        enterOrientation: "",
        isNew: false,
        contents: [],
      };

      alert("Container created and entered into Fleet Manager.");
    } catch (error) {
      console.error("Error creating & entering container:", error);
      alert("Failed to create & enter container.");
    }
  }

  function getProductName(productId) {
    const product = products.find((p) => p.id === productId);
    return product ? product.name : productId;
  }
</script>

<div class="space-y-8">
  <div class="card p-4">
    <h2 class="text-xl font-bold mb-4">Add New Container</h2>
    <form on:submit|preventDefault>
      <div>
        <label for="container-code" class="block">Container Code:</label>
        <input id="container-code" type="text" bind:value={newContainer.containerCode} class="w-full border p-2 rounded" />
      </div>
      <div>
        <label for="container-type" class="block">Type:</label>
        <select id="container-type" bind:value={newContainer.containerType} class="w-full border p-2 rounded">
          <option value="RACK">Rack</option>
          <option value="BIN">Bin</option>
        </select>
      </div>
      <div>
        <label for="container-position" class="block">Position:</label>
        <input id="container-position" type="text" bind:value={newContainer.position} class="w-full border p-2 rounded" />
      </div>
      <div>
        <label for="container-model-code" class="block">Container Model Code:</label>
        <input id="container-model-code" type="text" bind:value={newContainer.containerModelCode} class="w-full border p-2 rounded" />
      </div>
      <div>
        <label for="enter-orientation" class="block">Enter Orientation:</label>
        <input id="enter-orientation" type="text" bind:value={newContainer.enterOrientation} class="w-full border p-2 rounded" />
      </div>
      <div>
        <label class="block">Is New:</label>
        <input type="checkbox" bind:checked={newContainer.isNew} />
      </div>

      <!-- Add Products Section -->
      <div>
        <h3 class="text-lg font-bold mb-2">Add Products to Container</h3>
        <div class="space-y-2">
          {#each newContainer.contents as item, index (item.product_id)}
            <div class="flex items-center space-x-2">
              <select bind:value={item.product_id} class="w-full border p-2 rounded">
                <option value="" disabled>Select a product</option>
                {#each products as product}
                  <option value={product.id}>{product.name} (SKU: {product.sku})</option>
                {/each}
              </select>
              <input type="number" min="1" bind:value={item.quantity} placeholder="Quantity" class="w-24 border p-2 rounded" />
              <button type="button" on:click={() => removeProduct(index)} class="text-red-500">✕</button>
            </div>
          {/each}
          <button type="button" on:click={addProduct} class="text-blue-500">+ Add Product</button>
        </div>
      </div>

      <div class="flex space-x-4 mt-4">
        <button type="button" on:click={handleCreateContainer} class="bg-green-500 text-white px-4 py-2 rounded">Create</button>
        <button type="button" on:click={handleCreateAndEnterContainer} class="bg-blue-500 text-white px-4 py-2 rounded">Create & Enter</button>
      </div>
    </form>
  </div>
</div>
