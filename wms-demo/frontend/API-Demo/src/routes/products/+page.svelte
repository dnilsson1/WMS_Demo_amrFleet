<script>
  import { createProduct } from '$lib/api';
  import { onMount } from 'svelte';

  let newProduct = {
    id: '',
    name: '',
    sku: '',
    description: '',
    unit: 'pcs',
    minimum_stock: 0,
    current_stock: 0
  };

  let products = [];

  async function handleCreateProduct() {
    await createProduct(newProduct);
    newProduct = {
      id: '',
      name: '',
      sku: '',
      description: '',
      unit: 'pcs',
      minimum_stock: 0,
      current_stock: 0
    };
    await loadProducts(); // Refresh the product list after adding a new product
  }

  async function loadProducts() {
    const response = await fetch('http://127.0.0.1:8000/products/');
    products = await response.json();
  }

  onMount(() => {
    loadProducts();
  });
</script>

<h1 class="text-3xl font-bold mb-6">Create a New Product</h1>

<section class="container mx-auto p-4 h-[60vh]">
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4 h-full">
    <!-- Add New Product Section -->
    <div class="card p-4">
    
      <h2 class="text-xl font-bold mb-4">Add New Product</h2>
      <form on:submit|preventDefault={handleCreateProduct} class="space-y-4 flex-1">
        <div>
          <label for="product-id" class="block font-medium">ID:</label>
          <input id="product-id" type="text" bind:value={newProduct.id} class="w-full border p-2 rounded" />
        </div>
        <div>
          <label for="product-name" class="block font-medium">Name:</label>
          <input id="product-name" type="text" bind:value={newProduct.name} class="w-full border p-2 rounded" />
        </div>
        <div>
          <label for="product-sku" class="block font-medium">SKU:</label>
          <input id="product-sku" type="text" bind:value={newProduct.sku} class="w-full border p-2 rounded" />
        </div>
        <div>
          <label for="product-description" class="block font-medium">Description:</label>
          <textarea id="product-description" bind:value={newProduct.description} class="w-full border p-2 rounded"></textarea>
        </div>
        <div>
          <label for="product-unit" class="block font-medium">Unit:</label>
          <input id="product-unit" type="text" bind:value={newProduct.unit} class="w-full border p-2 rounded" />
        </div>
        <div>
          <label for="product-min-stock" class="block font-medium">Minimum Stock:</label>
          <input id="product-min-stock" type="number" bind:value={newProduct.minimum_stock} class="w-full border p-2 rounded" />
        </div>
        <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition duration-150">
          Create Product
        </button>
      </form>
    </div>

    <!-- Product List Section -->
    <div class="card p-4">
      <h2 class="text-xl font-bold mb-4">Existing Products</h2>
      {#if products.length > 0}
        <ul class="space-y-4 flex-1">
          {#each products as product}
            <li class="p-4 border rounded shadow">
              <h3 class="font-semibold text-lg">{product.name}</h3>
              <p><strong>SKU:</strong> {product.sku}</p>
              <p><strong>Description:</strong> {product.description}</p>
              <p><strong>Unit:</strong> {product.unit}</p>
              <p><strong>Minimum Stock:</strong> {product.minimum_stock}</p>
              <p><strong>Current Stock:</strong> {product.current_stock}</p>
            </li>
          {/each}
        </ul>
      {:else}
        <p>No products available.</p>
      {/if}
    </div>
  </div>
</section>

