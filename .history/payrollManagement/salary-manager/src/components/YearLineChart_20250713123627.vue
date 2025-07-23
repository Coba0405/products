<template>
    <!--  親要素の高さで可変にしたいなら h-64 とかを付ける  -->
    <Line
        ref="chartRef"
        :data="makeData()"
        :options="makeOptions"
        class="w-full" h-64
        height="300"
     />
</template>

<script setup>
import { reactive, toRaw, watch, onMounted, ref } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, LineElement, PointElement, LinearScale, CategoryScale, Legend, Title, Tooltip } from 'chart.js'

// 使用するパーツだけ登録
ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Legend, Title, Tooltip)

// 親から渡す props
const props = defineProps({
    labels: { type: Array, required: true },
    income: { type: Array, required: true },
    deduction: { type: Array, required: true },
    net: { type: Array, required: true }
})

const chartRef = ref(null)
const maxY = () =>  Math.max(...props.income, ...props.deduction, ...props.net)

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
        ]
    }
}

// 初期描画
onMounted(() => {
    chartRef.value.chart.update() 
})

watch(
    () => [props.income, props.deduction, props.net],
    () => {
        const c = chartRef.value.chart
        c.data = makeData()
        c.options = makeOptions()
        c.update()
    }
)

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
