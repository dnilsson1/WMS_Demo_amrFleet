<script>
  import { createProduct, adjustStock } from '$lib/api';
  import { onMount } from 'svelte';

  let product = {
    name: '',
    description: '',
    unit: 'pcs',
    minimum_stock: 0,
  };

  let products = [];

  async function handleAddProduct() {
    try {
      if (!product.name) {
        alert('Product name is required.');
        return;
      }
      const newProduct = await createProduct(product);
      alert(`Product created with SKU: ${newProduct.sku}`);
      product = {
        name: '',
        description: '',
        unit: 'pcs',
        minimum_stock: 0,
      };
      await loadProducts();
    } catch (error) {
      console.error('Error creating product:', error);
      alert('Failed to create product.');
    }
  }

  async function adjustProductStock(product) {
    const quantity = parseInt(product.adjustQuantity);
    if (isNaN(quantity) || quantity === 0) {
      alert('Please enter a valid non-zero quantity to adjust.');
      return;
    }

    try {
      const result = await adjustStock(product.id, quantity);
      alert(`Stock adjusted. New stock level: ${result.new_stock_level}`);
      product.adjustQuantity = 0;
      await loadProducts();
    } catch (error) {
      console.error('Error adjusting stock:', error);
      alert('Failed to adjust stock.');
    }
  }

  async function loadProducts() {
    try {
      const response = await fetch('http://127.0.0.1:8000/products/');
      if (!response.ok) {
        throw new Error(`Failed to load products: ${response.statusText}`);
      }
      const data = await response.json();
      products = data.map((p) => ({ ...p, adjustQuantity: 0 }));
    } catch (error) {
      console.error('Error loading products:', error);
      alert('Failed to load products.');
      products = [];
    }
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

      <form on:submit|preventDefault={handleAddProduct}>
        <!-- Name -->
        <div>
          <label for="product-name">Name:</label>
          <input id="product-name" type="text" bind:value={product.name} required />
        </div>

        <!-- Description (Optional) -->
        <div>
          <label for="product-description">Description:</label>
          <textarea id="product-description" bind:value={product.description}></textarea>
        </div>

        <!-- Unit (Optional or Defaulted) -->
        <div>
          <label for="product-unit">Unit:</label>
          <input id="product-unit" type="text" bind:value={product.unit} />
        </div>

        <!-- Minimum Stock (Optional) -->
        <div>
          <label for="product-min-stock">Minimum Stock:</label>
          <input id="product-min-stock" type="number" min="0" bind:value={product.minimum_stock} />
        </div>

        <!-- Submit Button -->
        <button type="submit">Add Product</button>
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

              <!-- Adjust Stock Section -->
              <div class="mt-4">
                <label for="adjust-quantity-{product.id}">Adjust Quantity:</label>
                <input
                  id="adjust-quantity-{product.id}"
                  type="number"
                  bind:value={product.adjustQuantity}
                  placeholder="Enter quantity"
                  class="border p-1 rounded w-24"
                />
                <button on:click={() => adjustProductStock(product)} class="bg-blue-500 text-white px-2 py-1 rounded ml-2">
                  Adjust Stock
                </button>
              </div>
            </li>
          {/each}
        </ul>
      {:else}
        <p>No products available.</p>
      {/if}
    </div>
  </div>
</section>
