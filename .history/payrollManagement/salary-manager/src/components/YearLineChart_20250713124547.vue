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
import {
  Chart,
  LineElement, PointElement,
  LinearScale, Title, Legend, Tooltip,
  CategoryScale
} from 'chart.js'
Chart.register(
  LineElement, PointElement,
  LinearScale, Title, Legend, Tooltip,
  CategoryScale
)

// 使用するパーツだけ登録
ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Legend, Title, Tooltip)

// 親から渡す props
const props = defineProps({
    labels: { type: Array, required: true },
    income: { type: Array, required: true },
    deduction: { type: Array, required: true },
    net: { type: Array, required: true }
})


// データ定義
function makeData () {
    return {
        labels: props.labels,
        datasets: [
            {
                label: '収入',
                data: toRaw(props.income),
                borderColor: '#e91e63',
                tension: 0.3
            },
            {
                label: '控除',
                data: toRaw(props.deduction),
                borderColor: '#ff9800',
                tension: 0.3
            },
            {
                label: '手取り',
                data: toRaw(props.net),
                borderColor: '#ffc107',
                tension: 0.3
            }
        ]
    }
}

function makeOptions () {
    return {
        responsive: true,
        maintainAspentRatio: false,
        scales: {
            y: {
                beginAtZero: true,
                suggestedMax: maxY() * 1.1,
                ticks: { callback: v => v.toLocaleString() },
                stepSize: 50000
            }
        }
    }
}
const chartData = reactive( makeData() )
const chartOptions = reactive( makeOptions() )

watch(
    () => [props.income, props.deduction, props.net],
    () => {
        Object.assign(chartData, makeData())
        Object.assign(chartOptions, makeOptions())
        if (chartRef.value?.chart) chartRef.value.chart.update()
    }
)

const chartRef = ref(null)

// 初期描画
onMounted(() => {
    // mounted時点でchartRef.value.chartが存在する
})

// Chart.js用のdataset
// const data = {
    //     labels: props.labels,
    //     datasets: [
        //         { label:'収入', data:props.income, borderColor:'#c026d3', backgroundColor:'#c026d3' },
//         { label:'控除', data:props.deduction,  borderColor:'#fb923c', backgroundColor:'#fb923c' },
//         { label:'手取り', data:props.net, borderColor:'#eab308', backgroundColor:'#eab308' }
//     ]
// }

// const options = {
//     responsive: true,
//     maintainAspectRatio: false,
//     tension: 0.3,
//     scales: {
//         y: { ticks: { callback:v=>v.toLocaleString() }}
//     }
// }
</script>
