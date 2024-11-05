<script>
    import { setContext } from "svelte";
    import { page } from "$app/stores";
  
    // Set API URL in context so all components can access it
    setContext("apiUrl", "http://localhost:8000");
  </script>
  
  <nav class="bg-gray-800 text-white p-4">
    <div class="container mx-auto flex gap-4">
      <a href="/" class="hover:text-gray-300">Products</a>
      <a href="/containers" class="hover:text-gray-300">Containers</a>
      <a href="/orders" class="hover:text-gray-300">Orders</a>
    </div>
  </nav>
  
  <main class="container mx-auto p-4">
    <slot />
  </main>