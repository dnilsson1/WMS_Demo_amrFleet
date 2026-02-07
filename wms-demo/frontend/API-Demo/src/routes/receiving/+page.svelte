<script>
  import { onMount } from "svelte";
  import { receivingScan } from "$lib/api";
  import { scanner } from "$lib/actions/scanner";

  let form = {
    product_sku: "",
    quantity: 1,
    container_code: "",
  };

  let isSubmitting = false;
  let successFlash = false;
  let errorMessage = "";
  let skuInput;
  let lastReceived = null;
  let successModalOpen = false;

  function resetForm() {
    form = {
      product_sku: "",
      quantity: 1,
      container_code: "",
    };
  }

  function normalizeErrorMessage(detail) {
    if (!detail) {
      return "Receiving failed.";
    }
    if (typeof detail === "string") {
      return detail;
    }
    if (typeof detail === "object") {
      return detail.message || detail.error || "Receiving failed.";
    }
    return "Receiving failed.";
  }

  async function handleSubmit() {
    errorMessage = "";

    const payload = {
      product_sku: (form.product_sku || "").trim(),
      quantity: Number(form.quantity),
      container_code: (form.container_code || "").trim(),
    };

    if (!payload.product_sku || !payload.container_code) {
      errorMessage = "Product SKU and container code are required.";
      return;
    }

    if (!Number.isFinite(payload.quantity) || payload.quantity <= 0) {
      errorMessage = "Quantity must be greater than zero.";
      return;
    }

    isSubmitting = true;
    try {
      const result = await receivingScan(payload);
      lastReceived = {
        product_id: result.product_id,
        product_sku: payload.product_sku,
      };
      successModalOpen = true;
      resetForm();
      successFlash = true;
      setTimeout(() => {
        successFlash = false;
      }, 700);
      skuInput?.focus();
    } catch (error) {
      errorMessage = normalizeErrorMessage(error?.detail || error?.message);
    } finally {
      isSubmitting = false;
    }
  }

  function handleScan(value) {
    form = {
      ...form,
      product_sku: value,
    };
    skuInput?.focus();
  }

  onMount(() => {
    skuInput?.focus();
  });
</script>

{#if successFlash}
  <div class="fixed inset-0 bg-green-500/20 pointer-events-none transition-opacity"></div>
{/if}

{#if errorMessage}
  <div class="fixed inset-0 bg-red-900/30 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-lg max-w-md w-full p-6 border border-red-200">
      <h2 class="text-xl font-bold text-red-700 mb-2">Receiving Error</h2>
      <p class="text-gray-800 mb-6">{errorMessage}</p>
      <div class="flex items-center justify-between">
        <a href="/products" class="text-blue-600 font-semibold">Create Product</a>
        <button
          type="button"
          class="bg-red-600 text-white px-4 py-2 rounded"
          on:click={() => (errorMessage = "")}
        >
          Close
        </button>
      </div>
    </div>
  </div>
{/if}

{#if successModalOpen && lastReceived}
  <div class="fixed inset-0 bg-green-900/20 flex items-center justify-center z-40">
    <div class="bg-white rounded-lg shadow-lg max-w-md w-full p-6 border border-green-200">
      <h2 class="text-xl font-bold text-green-700 mb-2">Receiving Complete</h2>
      <p class="text-gray-800 mb-6">SKU {lastReceived.product_sku} added successfully.</p>
      <div class="flex items-center justify-between">
        <a
          href={`/api/products/${lastReceived.product_id}/label`}
          target="_blank"
          class="text-blue-600 font-semibold"
          rel="noreferrer"
        >
          Print Label
        </a>
        <button
          type="button"
          class="bg-green-600 text-white px-4 py-2 rounded"
          on:click={() => (successModalOpen = false)}
        >
          Close
        </button>
      </div>
    </div>
  </div>
{/if}

<div class="space-y-6" use:scanner={{ target: skuInput, onScan: handleScan }}>
  <div class="card p-4">
    <h1 class="text-3xl font-bold mb-2">Inbound Receiving</h1>
    <p class="text-gray-600">Scan or enter a product SKU, quantity, and target container.</p>
  </div>

  <div class="card p-4">
    <form on:submit|preventDefault={handleSubmit} class="space-y-4">
      <div>
        <label for="sku" class="block">Product SKU</label>
        <input
          id="sku"
          type="text"
          bind:value={form.product_sku}
          bind:this={skuInput}
          autocomplete="off"
          class="w-full border p-2 rounded"
        />
      </div>

      <div>
        <label for="quantity" class="block">Quantity</label>
        <input
          id="quantity"
          type="number"
          min="1"
          bind:value={form.quantity}
          class="w-full border p-2 rounded"
        />
      </div>

      <div>
        <label for="container" class="block">Target Container</label>
        <input
          id="container"
          type="text"
          bind:value={form.container_code}
          autocomplete="off"
          class="w-full border p-2 rounded"
        />
      </div>

      <div class="flex items-center gap-4">
        <button
          type="submit"
          class="bg-green-600 text-white px-4 py-2 rounded"
          disabled={isSubmitting}
        >
          {isSubmitting ? "Receiving..." : "Receive"}
        </button>
        <button
          type="button"
          class="bg-gray-200 text-gray-800 px-4 py-2 rounded"
          on:click={resetForm}
        >
          Reset
        </button>
      </div>
    </form>
  </div>
</div>
