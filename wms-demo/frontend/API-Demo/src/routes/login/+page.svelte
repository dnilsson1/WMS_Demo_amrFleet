<script>
  let username = "";
  let password = "";
  let errorMessage = "";
  let isSubmitting = false;

  async function handleLogin() {
    errorMessage = "";
    if (!username || !password) {
      errorMessage = "Username and password are required.";
      return;
    }

    isSubmitting = true;
    try {
      const body = new URLSearchParams({
        username,
        password,
      });
      const response = await fetch("/api/auth/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Login failed");
      }

      const data = await response.json();
      document.cookie = `access_token=${data.access_token}; Path=/; SameSite=Lax`;
      window.location.href = "/";
    } catch (error) {
      errorMessage = error?.message || "Login failed.";
    } finally {
      isSubmitting = false;
    }
  }
</script>

<div class="min-h-[70vh] flex items-center justify-center">
  <div class="card p-6 w-full max-w-md">
    <h1 class="text-3xl font-bold mb-2">Sign In</h1>
    <p class="text-gray-600 mb-6">Use your warehouse credentials to continue.</p>

    <form on:submit|preventDefault={handleLogin} class="space-y-4">
      <div>
        <label for="username" class="block font-medium">Username</label>
        <input id="username" type="text" bind:value={username} class="w-full border p-2 rounded" />
      </div>

      <div>
        <label for="password" class="block font-medium">Password</label>
        <input id="password" type="password" bind:value={password} class="w-full border p-2 rounded" />
      </div>

      {#if errorMessage}
        <div class="bg-red-100 text-red-700 p-2 rounded">{errorMessage}</div>
      {/if}

      <button
        type="submit"
        class="bg-blue-600 text-white font-semibold py-2 px-6 rounded hover:bg-blue-700 transition duration-200"
        disabled={isSubmitting}
      >
        {isSubmitting ? "Signing in..." : "Sign In"}
      </button>
    </form>

    <p class="text-sm text-gray-500 mt-4">Ask your admin for credentials.</p>
  </div>
</div>
