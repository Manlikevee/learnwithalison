/* ================= COMMON ================= */
const bodyFont = getComputedStyle(document.body).fontFamily.trim();

/* Helper: random data */
function generateRandomData(min, max, length = 12) {
  return Array.from({ length }, () =>
    Math.floor(Math.random() * (max - min + 1)) + min
  );
}

/* ================= MULTI PIE (DOUGHNUT) ================= */
new CustomChartJs({
  selector: "#multi-pie-chart",
  options: () => ({
    type: "doughnut",
    data: {
      labels: [
        "Online Store",
        "Retail Stores",
        "B2B Revenue",
        "Marketplace Revenue"
      ],
      datasets: [
        {
          label: "2024",
          data: [300, 150, 100, 80],
          backgroundColor: [
            ins("chart-primary"),
            ins("chart-secondary"),
            ins("chart-dark"),
            ins("chart-gray")
          ],
          borderColor: "transparent",
          borderWidth: 1,
          cutout: "30%",
          radius: "90%"
        },
        {
          label: "2023",
          data: [270, 135, 90, 72],
          backgroundColor: [
            ins("chart-primary-rgb", 0.3),
            ins("chart-secondary-rgb", 0.3),
            ins("chart-dark-rgb", 0.3),
            ins("chart-gray-rgb", 0.3)
          ],
          borderColor: "transparent",
          borderWidth: 3,
          cutout: "30%",
          radius: "60%"
        }
      ]
    },
    options: {
      plugins: {
        legend: {
          position: "bottom",
          labels: {
            font: { family: bodyFont },
            color: ins("secondary-color"),
            usePointStyle: true,
            pointStyle: "circle",
            boxWidth: 8,
            boxHeight: 8,
            padding: 15
          }
        },
        tooltip: {
          callbacks: {
            label(ctx) {
              return `${ctx.dataset.label} - ${ctx.label}: ${ctx.parsed}`;
            }
          }
        }
      },
      scales: {
        x: { display: false },
        y: { display: false }
      }
    }
  })
});

/* ================= SALES ANALYTICS ================= */
const months = [
  "Jan","Feb","Mar","Apr","May","Jun",
  "Jul","Aug","Sep","Oct","Nov","Dec"
];

const onlineSales   = generateRandomData(1000, 1250);
const inStoreSales  = generateRandomData(800, 1250);
const totalSales    = generateRandomData(2500, 3500);

new CustomChartJs({
  selector: "#sales-analytics-chart",
  options: () => ({
    data: {
      labels: months,
      datasets: [
        {
          type: "bar",
          label: "Online Sales",
          data: onlineSales,
          backgroundColor: ins("chart-primary"),
          borderColor: ins("chart-primary"),
          stack: "sales",
          barThickness: 20,
          borderRadius: 6
        },
        {
          type: "bar",
          label: "In-store Sales",
          data: inStoreSales,
          backgroundColor: ins("chart-gray"),
          borderColor: ins("chart-gray"),
          stack: "sales",
          barThickness: 20,
          borderRadius: 6
        },
        {
          type: "line",
          label: "Projected Sales",
          data: totalSales,
          borderColor: ins("chart-dark"),
          backgroundColor: ins("chart-dark-rgb", 0.2),
          borderWidth: 2,
          borderDash: [5, 5],
          tension: 0.4,
          fill: false,
          yAxisID: "y"
        }
      ]
    }
  })
});