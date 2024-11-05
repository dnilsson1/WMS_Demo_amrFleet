<script>
    import { onMount } from 'svelte';
    import { createProduct, adjustStock } from "$lib/api";
    
    let products = [];
    let newProduct = {
        name: '',
        sku: '',
        description: '',
        unit: 'pcs',
        minimum_stock: 0,
        current_stock: 0
    };
    
    let adjustmentData = {
        productId: '',
        quantity: 0,
        containerCode: ''
    };
    
    onMount(async () => {
        await loadProducts();
    });
    
    async function loadProducts() {
        const response = await fetch('/products/');
        products = await response.json();
    }
    
    async function handleCreateProduct() {
        await createProduct(newProduct);
        await loadProducts();
        newProduct = {
            name: '',
            sku: '',
            description: '',
            unit: 'pcs',
            minimum_stock: 0,
            current_stock: 0
        };
    }
    
    async function handleAdjustStock() {
        await adjustStock(
            adjustmentData.productId,
            adjustmentData.quantity,
            adjustmentData.containerCode
        );
        await loadProducts();
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
        
        <div class="bg-white p-4 rounded shadow">
            <h2 class="text-xl font-bold mb-4">Adjust Stock</h2>
            <form on:submit|preventDefault={handleAdjustStock} class="space-y-4">
                <div>
                    <label for="adjustment-product" class="block">Product:</label>
                    <select id="adjustment-product" bind:value={adjustmentData.productId} class="w-full border p-2 rounded">
                        {#each products as product}
                            <option value={product.id}>{product.name}</option>
                        {/each}
                    </select>
                </div>
                <div>
                    <label for="adjustment-quantity" class="block">Quantity:</label>
                    <input id="adjustment-quantity" type="number" bind:value={adjustmentData.quantity} class="w-full border p-2 rounded" />
                </div>
                <div>
                    <label for="adjustment-container" class="block">Container Code:</label>
                    <input id="adjustment-container" type="text" bind:value={adjustmentData.containerCode} class="w-full border p-2 rounded" />
                </div>
                <button type="submit" class="bg-green-500 text-white px-4 py-2 rounded">
                    Adjust Stock
                </button>
            </form>
        </div>
    </div>
    
    <div class="mt-8">
        <h2 class="text-xl font-bold mb-4">Product List</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            {#each products as product}
                <div class="bg-white p-4 rounded shadow">
                    <h3 class="font-bold">{product.name}</h3>
                    <p class="text-gray-600">SKU: {product.sku}</p>
                    <p class="text-gray-600">Current Stock: {product.current_stock} {product.unit}</p>
                    <p class="text-gray-600">Minimum Stock: {product.minimum_stock} {product.unit}</p>
                    {#if product.description}
                        <p class="text-gray-600 mt-2">{product.description}</p>
                    {/if}
                </div>
            {/each}
        </div>
    </div>
</div>