<script>
    import { createProduct } from '../api.js';
    let newProduct = {
      name: '',
      sku: '',
      description: '',
      unit: 'pcs',
      minimum_stock: 0,
      current_stock: 0
    };
  
    async function handleCreateProduct() {
      await createProduct(newProduct);
      // Add your loadProducts function here if needed
      newProduct = {
        name: '',
        sku: '',
        description: '',
        unit: 'pcs',
        minimum_stock: 0,
        current_stock: 0
      };
    }
  </script>
  
  <div class="container mx-auto p-4">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="bg-white p-4 rounded shadow">
        <h2 class="text-xl font-bold mb-4">Add New Product</h2>
        <form on:submit|preventDefault={handleCreateProduct} class="space-y-4">
          <div>
            <label for="product-name" class="block">Name:</label>
            <input id="product-name" type="text" bind:value={newProduct.name} class="w-full border p-2 rounded" />
          </div>
          <div>
            <label for="product-sku" class="block">SKU:</label>
            <input id="product-sku" type="text" bind:value={newProduct.sku} class="w-full border p-2 rounded" />
          </div>
          <div>
            <label for="product-description" class="block">Description:</label>
            <textarea id="product-description" bind:value={newProduct.description} class="w-full border p-2 rounded"></textarea>
          </div>
          <div>
            <label for="product-unit" class="block">Unit:</label>
            <input id="product-unit" type="text" bind:value={newProduct.unit} class="w-full border p-2 rounded" />
          </div>
          <div>
            <label for="product-min-stock" class="block">Minimum Stock:</label>
            <input id="product-min-stock" type="number" bind:value={newProduct.minimum_stock} class="w-full border p-2 rounded" />
          </div>
          <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">
            Create Product
          </button>
        </form>
      </div>
    </div>
  </div>
  