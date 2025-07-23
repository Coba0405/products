<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart, LineElement, PointElement, LinearScale,
  CategoryScale, Title, Legend, Tooltip
} from 'chart.js'

Chart.register(LineElement, PointElement, LinearScale,
               CategoryScale, Title, Legend, Tooltip)

// ---------- props ----------
const props = defineProps({
  labels:    { type: Array, default: () => [] },
  income:    { type: Array, default: () => [] },
  deduction: { type: Array, default: () => [] },
  net:       { type: Array, default: () => [] },
  title: { type: String, default: '' }
})

// ---------- computed でそのまま渡す ----------
const chartData = computed(() => ({
  labels: props.labels,
  datasets: [
    {
      label: '収入',
      data:   props.income,
      borderColor: '#42a5f5',
      tension: 0
    },
    {
      label: '控除',
      data:   props.deduction,
      borderColor: '#ef5350',
      tension: 0
    },
    {
      label: '手取り',
      data:   props.net,
      borderColor: '#66bb6a',
      tension: 0
    }
  ]
}))

const chartOptions = computed(() => {
  const max = Math.max(
    ...props.income, ...props.deduction, ...props.net, 1
  )
  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      title: {
        display: true,
        text: props.title || `${props.labels[0] ?? ''}〜${props.labels[11] ??''} 推移` },
      legend:{ position:'top' }
    },
    scales: {
      y: {
        beginAtZero: true,
        suggestedMax: max * 1.1,
        ticks: { callback:v => Number(v).toLocaleString() }
      }
    }
  }
})
</script>

<template>
  <div class="h-[350px]">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>