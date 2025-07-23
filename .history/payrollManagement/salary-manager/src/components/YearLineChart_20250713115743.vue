<template>
    <!--  親要素の高さで可変にしたいなら h-64 とかを付ける  -->
    <Line :data="data" :options="options" class="w-full" h-64 />
</template>

<script setup>
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

function makeOptions () {
    return {
        responsive: true,
        maintainAspentRatio: false,
        scales: {
            y: {
                
            }
        }
    }
}

// Chart.js用のdataset
const data = {
    labels: props.labels,
    datasets: [
        { label:'収入', data:props.income, borderColor:'#c026d3', backgroundColor:'#c026d3' },
        { label:'控除', data:props.deduction,  borderColor:'#fb923c', backgroundColor:'#fb923c' },
        { label:'手取り', data:props.net, borderColor:'#eab308', backgroundColor:'#eab308' }
    ]
}

const options = {
    responsive: true,
    maintainAspectRatio: false,
    tension: 0.3,
    scales: {
        y: { ticks: { callback:v=>v.toLocaleString() }}
    }
}
    console.log('income', props.income)
    console.log('deduct', props.deduction)
    console.log('typeof', typeof props.income[0])
</script>
