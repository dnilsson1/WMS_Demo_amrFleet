<script>
  import { onMount } from "svelte";
  import Chart from "chart.js/auto";

  let chartCanvas;
  let chartInstance;
  let refreshTimer;

  async function loadThroughput() {
    const response = await fetch("/api/analytics/throughput");
    if (!response.ok) {
      return;
    }
    const payload = await response.json();
    const data = payload.data || [];
    const labels = data.map((item) =>
      new Date(item.hour).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    );
    const counts = data.map((item) => item.count);

    if (!chartInstance) {
      chartInstance = new Chart(chartCanvas, {
        type: "line",
        data: {
          labels,
          datasets: [
            {
              label: "Movements per Hour",
              data: counts,
              borderColor: "#0f766e",
              backgroundColor: "rgba(13, 148, 136, 0.2)",
              tension: 0.3,
              fill: true,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });
    } else {
      chartInstance.data.labels = labels;
      chartInstance.data.datasets[0].data = counts;
      chartInstance.update();
    }
  }

  onMount(async () => {
    await loadThroughput();
    refreshTimer = setInterval(loadThroughput, 60000);
    return () => {
      clearInterval(refreshTimer);
      chartInstance?.destroy();
    };
  });
</script>

<div class="space-y-8">
  <div class="card p-6 bg-gradient-to-br from-emerald-50 via-teal-50 to-slate-50">
    <h1 class="text-4xl font-bold mb-2">Operations Snapshot</h1>
    <p class="text-gray-600">Last 24 hours of inbound and outbound movement volume.</p>
  </div>

  <div class="card p-6">
    <h2 class="text-2xl font-semibold mb-4">Movements per Hour</h2>
    <div class="h-80">
      <canvas bind:this={chartCanvas}></canvas>
    </div>
  </div>
</div>

