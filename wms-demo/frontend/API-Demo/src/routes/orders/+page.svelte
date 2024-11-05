<script>
  import { onMount } from "svelte";
  import { createOrder, pickOrder, getProducts } from "$lib/api";
  
  let orders = [];
  let products = [];
  let orderItems = [{ product_id: "", quantity: 1 }];
  
  onMount(async () => {
    products = await getProducts();
  });

  async function handleCreateOrder() {
    const order = await createOrder(orderItems);
    orderItems = [{ product_id: "", quantity: 1 }];
    // Reload orders
  }

  function addOrderItem() {
    orderItems = [...orderItems, { product_id: "", quantity: 1 }];
  }
</script>

<div class="space-y-8">
  <div class="bg-white p-4 rounded shadow">
    <h2 class="text-xl font-bold mb-4">Create New Order</h2>
    <form on:submit|preventDefault={handleCreateOrder} class="space-y-4">
      {#each orderItems as item, i}
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block">Product:</label>
            <select bind:value={item.product_id} class="w-full border p-2 rounded">
              <option value="">Select Product</option>
              {#each products as product}
                <option value={product.id}>{product.name}</option>
              {/each}
            </select>
          </div>
          <div>
            <label class="block">Quantity:</label>
            <input type="number" bind:value={item.quantity} min="1" class="w-full border p-2 rounded" />
          </div>
        </div>
      {/each}
      
      <div class="flex gap-4">
        <button type="button" on:click={addOrderItem} class="bg-gray-500 text-white px-4 py-2 rounded">
          Add Item
        </button>
        <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">
          Create Order
        </button>
      </div>
    </form>
  </div>
</div>