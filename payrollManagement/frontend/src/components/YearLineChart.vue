<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart, LineElement, PointElement, LinearScale,
  CategoryScale, Title, Legend, Tooltip
} from 'chart.js'

Chart.register(LineElement, PointElement, LinearScale,
               CategoryScale, Title, Legend, Tooltip)

Tooltip.positioners.offsetAbove = function (items, eventPosition) {
  if (!items.length) return false
  const isRightSide = eventPosition.x > this.chart.width * 0.6
  return {
    x: eventPosition.x + (isRightSide ? -40 : 40),
    y: eventPosition.y - 40,
    xAlign: isRightSide ? 'right' : 'left'
  }
}

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
      backgroundColor: '#42a5f520',
      tension: 0,
      pointRadius: 5,
      pointHoverRadius: 8
    },
    {
      label: '控除',
      data:   props.deduction,
      borderColor: '#ef5350',
      backgroundColor: '#ef535020',
      tension: 0,
      pointRadius: 5,
      pointHoverRadius: 8
    },
    {
      label: '手取り',
      data:   props.net,
      borderColor: '#66bb6a',
      backgroundColor: '#66bb6a20',
      tension: 0,
      pointRadius: 5,
      pointHoverRadius: 8
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
    interaction: {
      mode: 'index',
      intersect: false
    },
    plugins: {
      title: {
        display: true,
        text: props.title ||
          (props.labels.length
            ? `${props.labels[0] ?? ''}〜${props.labels[props.labels.length - 1] ??''} 推移`
          : '')
      },
      legend: { position: 'top' },
      tooltip: {
        mode: 'index',
        intersect: false,
        position: 'offsetAbove',
        callbacks: {
          label: ctx => ` ${ctx.dataset.label}: ${Number(ctx.parsed.y).toLocaleString()} 円`
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        suggestedMax: max * 1.1,
        ticks: { callback: v => Number(v).toLocaleString() }
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