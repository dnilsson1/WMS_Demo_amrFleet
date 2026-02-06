<script>
  import "../app.css";
  import { AppRail, AppRailAnchor } from '@skeletonlabs/skeleton';
  import { page } from '$app/stores';

  import homeIcon from '../assets/home.svg';
  import productsIcon from '../assets/products.svg';
  import palletIcon from '../assets/pallet.svg';
  import forkliftIcon from '../assets/forklift.svg';
  import settingsIcon from '../assets/settings.svg';

</script>

  <div class="flex flex-col min-h-screen overflow-hidden">
  <div class="flex h-full flex-1">
  <!-- App Rail Navigation -->
  <AppRail class="w-20 h-full">
    <AppRailAnchor href="/" selected={$page.url.pathname === '/'} label="Home">
      <svelte:fragment slot="lead">
        <img src={homeIcon} alt="Home Icon" class="h-6 w-6" />
      </svelte:fragment>
    </AppRailAnchor>

    <AppRailAnchor href="/products" selected={$page.url.pathname === '/products'} label="Products">
      <svelte:fragment slot="lead">
        <img src={productsIcon} alt="Products Icon" class="h-6 w-6" />
      </svelte:fragment>
    </AppRailAnchor>

    <AppRailAnchor href="/containers" selected={$page.url.pathname === '/containers'} label="Containers">
      <svelte:fragment slot="lead">
        <img src={palletIcon} alt="Containers Icon" class="h-6 w-6" />
      </svelte:fragment>
    </AppRailAnchor>

    <AppRailAnchor href="/orders" selected={$page.url.pathname === '/orders'} label="Orders">
      <svelte:fragment slot="lead">
        <img src={forkliftIcon} alt="Orders Icon" class="h-6 w-6" />
      </svelte:fragment>
    </AppRailAnchor>

  <AppRailAnchor href="/settings" selected={$page.url.pathname === '/settings'} label="Settings">
    <svelte:fragment slot="lead">
      <img src={settingsIcon} alt="Settings Icon" class="h-6 w-6" />
    </svelte:fragment>
  </AppRailAnchor>
</AppRail>


  <!-- Main Content Area -->
  <main class="flex-1 container mx-auto p-4 overflow-hidden">
    <slot />
  </main>
</div>

<!-- Footer -->
<footer class="bg-gray-800 text-white p-4 mt-8">
  <p class="text-center">&copy; 2024 Warehouse Management System Demo by Daniel Nilsson</p>
</footer>
</div>
