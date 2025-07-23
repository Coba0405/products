<template>
    <div class="h-[350px]">      <!-- 固定高さをあげても OK -->
    <Line
      ref="chartRef"
      :data="chartData"
      :options="chartOptions"
    />
  </div>
</template>

<script setup>
import { Chart, LineElement, PointElement, LinearScale, Title, Legend, Tooltip, CategoryScale } from 'chart.js'
Chart.register( LineElement, PointElement, LinearScale, Title, Legend, Tooltip, CategoryScale )

import { Line } from 'vue-chartjs'
import { reactive, watch, onMounted, ref, toRaw } from 'vue'

/* ---------- props ---------- */
const props = defineProps({
  labels:     { type:Array, default:()=>[] },
  income:     { type:Array, default:()=>[] },
  deduction:  { type:Array, default:()=>[] },
  net:        { type:Array, default:()=>[] }
})

/* ---------- データ ---------- */
function buildData () {
  return {
    labels: props.labels,
    datasets: [
      {
        label: '収入',
        data: toRaw(props.income),
        borderColor: '#42a5f5',
        backgroundColor: 'transparent',
        tension: .3
      },
      {
        label: '控除',
        data: toRaw(props.deduction),
        borderColor: '#ef5350',
        backgroundColor: 'transparent',
        tension: .3
      },
      {
        label: '手取り',
        data: toRaw(props.net),
        borderColor: '#66bb6a',
        backgroundColor: 'transparent',
        tension: .3
      }
    ]
  }
}

/* ---------- オプション ---------- */
function buildOptions () {
  const max = Math.max(...props.income, ...props.deduction, ...props.net, 1)
  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      tooltip: { mode: 'index', intersect: false },
      legend:  { position: 'top' },
      title:   { display:true, text:`${props.labels?.[0]?.split('月')[0] ?? ''} 年推移` }
    },
    scales: {
      y: {
        beginAtZero: true,
        suggestedMax: max * 1.1,
        ticks: {
          callback: v => Number(v).toLocaleString()
        }
      }
    }
  }
}

/* ---------- reactive state ---------- */
const chartData    = reactive( buildData() )
const chartOptions = reactive( buildOptions() )

/* ---------- Chart インスタンス ---------- */
const chartRef = ref(null)

/* ---------- 変化を監視して再描画 ---------- */
watch(
  () => [props.labels, props.income, props.deduction, props.net],
  () => {
    Object.assign(chartData,    buildData())
    Object.assign(chartOptions, buildOptions())
    // Chart.js インスタンスが出来てから update
    chartRef.value?.chart?.update()
  },
  { deep:true }
)

/* ---------- mounted ---------- */
onMounted(() => {
  // 初回描画後に update する必要があればここで chart.update()
})
</script>
