<script>
  import { page } from '$app/stores';
</script>

<!-- Hero Section -->
<div class="card p-4 bg-gradient-to-br variant-gradient-secondary-tertiary">
  <div class="container mx-auto text-center">
    <h1 class="text-5xl font-bold mb-4">Welcome to the Warehouse Management System Demo</h1>
    <p class="text-lg mb-8">Manage your products, containers, and orders seamlessly with our intuitive interface.</p>
    <a href="/products" class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition inline-block">Get Started</a>
  </div>
</div>

<!-- Features Section -->
<div class="container mx-auto grid grid-cols-1 md:grid-cols-3 gap-8 py-16">
  <div class="card p-4">
    <h2 class="text-2xl font-semibold mb-4">Products</h2>
    <p class="mb-4">Add, manage, and track your products with ease. Keep inventory up to date.</p>
    <a href="/products" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition inline-block">Manage Products</a>
  </div>

  <div class="card p-4">
    <h2 class="text-2xl font-semibold mb-4">Containers</h2>
    <p class="mb-4">Organize your products into containers for efficient storage and tracking.</p>
    <a href="/containers" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition inline-block">View Containers</a>
  </div>

  <div class="card p-4">
    <h2 class="text-2xl font-semibold mb-4">Orders</h2>
    <p class="mb-4">Create, manage, and track customer orders with real-time inventory insights.</p>
    <a href="/orders" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition inline-block">Manage Orders</a>
  </div>
</div>

<!-- CTA Section -->
<div class="card p-4">
  <div class="container mx-auto text-center">
    <h2 class="text-3xl font-bold mb-6">Ready to streamline your warehouse management?</h2>
    <p class="mb-8">Our system helps you stay organized and efficient. Click below to learn more and get started.</p>
    <a href="/products" class="bg-blue-600 text-white px-6 py-3 rounded hover:bg-blue-700 transition inline-block">Start Managing Now</a>
  </div>
</div>

