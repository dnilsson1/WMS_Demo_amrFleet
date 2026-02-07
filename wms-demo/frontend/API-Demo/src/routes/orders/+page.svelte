<script>
  import { onMount } from "svelte";
  import { createOrder, pickOrder, getProducts, getOrders, cancelOrder } from "$lib/api";
  
  let orders = [];
  let products = [];
  let orderItems = [{ product_id: "", quantity: 1 }];
  let destinationName = ""; // For picking orders
  let refreshTimer;

  const statusLabels = {
    pending: "Pending",
    confirmed: "Confirmed",
    picking: "Robot Moving",
    completed: "Done",
    cancelled: "Cancelled",
    failed: "Failed",
  };

  function statusClass(status) {
    if (status === "completed") {
      return "bg-green-100 text-green-700";
    }
    if (status === "failed") {
      return "bg-red-100 text-red-700";
    }
    if (status === "cancelled") {
      return "bg-slate-100 text-slate-700";
    }
    if (status === "picking") {
      return "bg-blue-100 text-blue-700";
    }
    if (status === "confirmed") {
      return "bg-amber-100 text-amber-700";
    }
    return "bg-gray-100 text-gray-700";
  }

  async function refreshOrders() {
    orders = await getOrders();
  }

  onMount(async () => {
    products = await getProducts();
    await refreshOrders();
    refreshTimer = setInterval(refreshOrders, 5000);
    return () => {
      clearInterval(refreshTimer);
    };
  });

  async function handleCreateOrder() {
    const cleanedItems = orderItems
      .map((item) => ({
        product_id: (item.product_id || "").trim(),
        quantity: Number(item.quantity)
      }))
      .filter((item) => item.product_id && Number.isFinite(item.quantity) && item.quantity > 0);

    if (cleanedItems.length === 0) {
      alert("Please select at least one product with a valid quantity.");
      return;
    }

    try {
      const orderData = { items: cleanedItems };
      await createOrder(orderData);
      orderItems = [{ product_id: "", quantity: 1 }];
      // Reload orders
      await refreshOrders();
    } catch (error) {
      console.error("Error creating order:", error);
      alert(error?.message || "Failed to create order.");
    }
  }

  function addOrderItem() {
    orderItems = [...orderItems, { product_id: "", quantity: 1 }];
  }

  async function handlePickOrder(orderId) {
    if (!destinationName) {
      alert("Please enter a destination name.");
      return;
    }
    try {
      await pickOrder(orderId, destinationName);
      // Reload orders
      await refreshOrders();
    } catch (error) {
      console.error("Error picking order:", error);
      alert(error?.message || "Failed to pick order.");
    }
  }

  async function handleCancelOrder(orderId) {
    const confirmed = window.confirm("Cancel this order? The robot mission will be stopped.");
    if (!confirmed) {
      return;
    }
    try {
      await cancelOrder(orderId);
      await refreshOrders();
    } catch (error) {
      console.error("Error cancelling order:", error);
      alert(error?.message || "Failed to cancel order.");
    }
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
          <div class="flex items-center gap-3">
            <span class="font-semibold">Status:</span>
            <span class={`px-2 py-1 rounded text-sm font-semibold ${statusClass(order.status)}`}>
              {statusLabels[order.status] || order.status}
            </span>
          </div>
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
          {#if order.status === 'confirmed' || order.status === 'picking'}
            <button
              on:click={() => handleCancelOrder(order.orderId)}
              class="bg-red-600 text-white px-4 py-2 rounded ml-2"
            >
              Cancel Order
            </button>
          {/if}
          {#if order.status === 'picking'}
            <p class="text-sm text-gray-600">Order is active with the robot.</p>
          {/if}
          {#if order.status === 'completed'}
            <p class="text-sm text-gray-600">Order completed.</p>
          {/if}
          {#if order.status === 'failed'}
            <p class="text-sm text-red-600">Order failed in fleet manager.</p>
          {/if}
          {#if order.status === 'cancelled'}
            <p class="text-sm text-gray-600">Order was cancelled.</p>
          {/if}
        </div>
      {/each}
    </div>
  </div>
  
</div>