<script>
  import { onMount } from "svelte";
  import { createOrder, pickOrder, getProducts, getOrders } from "$lib/api";
  
  let orders = [];
  let products = [];
  let orderItems = [{ product_id: "", quantity: 1 }];
  let destinationName = ""; // For picking orders

  onMount(async () => {
    products = await getProducts();
    orders = await getOrders();
  });

  async function handleCreateOrder() {
    const orderData = { items: orderItems };
    const order = await createOrder(orderData);
    orderItems = [{ product_id: "", quantity: 1 }];
    // Reload orders
    orders = await getOrders();
  }

  function addOrderItem() {
    orderItems = [...orderItems, { product_id: "", quantity: 1 }];
  }

  async function handlePickOrder(orderId) {
    if (!destinationName) {
      alert("Please enter a destination name.");
      return;
    }
    await pickOrder(orderId, destinationName);
    // Reload orders
    orders = await getOrders();
  }
</script>


<div class="space-y-8">
  <div class="card p-4">
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
  
  <div class="card p-4">
    <h2 class="text-xl font-bold mb-4">Existing Orders</h2>
    <div>
      {#each orders as order}
        <div class="border p-4 mb-4">
          <h3 class="font-bold">Order ID: {order.orderId}</h3>
          <p>Status: {order.status}</p>
          <ul>
            {#each order.items as item}
              <li>
                Product ID: {item.product_id}, Quantity: {item.quantity}
              </li>
            {/each}
          </ul>
          {#if order.status === 'confirmed'}
            <input
              type="text"
              placeholder="Destination Name"
              bind:value={destinationName}
              class="border p-2 rounded mr-2"
            />
            <button on:click={() => handlePickOrder(order.orderId)} class="bg-green-500 text-white px-4 py-2 rounded">
              Pick Order
            </button>
          {/if}
          {#if order.status === 'picking'}
            <p>Order is being picked.</p>
          {/if}
          {#if order.status === 'completed'}
            <p>Order is completed.</p>
          {/if}
        </div>
      {/each}
    </div>
  </div>
  
</div>