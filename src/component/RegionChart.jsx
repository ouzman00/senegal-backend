"use client";

import React, { useMemo } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

let registered = false;
if (!registered) {
  ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);
  registered = true;
}

function norm(v) {
  return String(v ?? "").trim().toLowerCase();
}

export default function RegionChart({ regionsData = [], selectedRegion = null }) {
  const rows = useMemo(() => {
    const arr = Array.isArray(regionsData) ? regionsData : [];
    const cleaned = arr
      .map((r) => ({
        name: r?.name ?? "",
        superficie: Number(r?.superficie ?? 0) || 0,
      }))
      .filter((r) => r.name);

    cleaned.sort((a, b) => b.superficie - a.superficie);
    return cleaned;
  }, [regionsData]);

  if (!rows.length) return null;

  const sel = norm(selectedRegion);

  const data = {
    labels: rows.map((r) => r.name),
    datasets: [
      {
        label: "Superficie (km²)",
        data: rows.map((r) => r.superficie),
        backgroundColor: rows.map((r) =>
          norm(r.name) === sel ? "rgba(255, 99, 132, 0.9)" : "rgba(54, 162, 235, 0.6)"
        ),
        borderColor: rows.map((r) =>
          norm(r.name) === sel ? "rgb(255, 99, 132)" : "rgba(54, 162, 235, 1)"
        ),
        borderWidth: rows.map((r) => (norm(r.name) === sel ? 3 : 1)),
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    animation: false,
    plugins: {
      legend: { display: true, position: "top" },
      tooltip: {
        callbacks: {
          label: (ctx) => `${Number(ctx.parsed?.y ?? 0).toLocaleString()} km²`,
        },
      },
      datalabels: { display: false },
    },
    scales: {
      y: {
        beginAtZero: true,
        title: { display: true, text: "Superficie (km²)" },
        ticks: { callback: (v) => Number(v).toLocaleString() },
      },
      x: {
        title: { display: true, text: "Régions" },
        ticks: { autoSkip: true, maxRotation: 45, minRotation: 0 },
      },
    },
  };

  return (
    <div className="p-4 bg-white rounded-xl shadow-md border border-gray-300 h-[260px] sm:h-[300px]">
      <h3 className="font-semibold mb-2">Superficie des régions</h3>
      <Bar data={data} options={options} />
    </div>
  );
}
