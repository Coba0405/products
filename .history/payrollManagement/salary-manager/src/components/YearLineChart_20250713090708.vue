<template>
    <!--  親要素の高さで可変にしたいなら h-64 とかを付ける  -->
    <Line :data="data" :options="optopns" class="w-full" h-64 />
</template>

<script setup>
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, LineElement, PointElement, LinearScale, CategoryScale, Legend, Title, Tooltip, PointElement } from 'chart.js'

// 使用するパーツだけ登録
ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Legend, Title, Tooltip)

// 親から渡す props
const props = defineProps({
    labels: { type: Array, required: true },
    income: { type: Array, required: true },
    deduction: { type: Array, required: true },
    net: { type: Array, required: true }
})

// Chart.js用のdataset
const data = {
    labels: props.labels,
    datasets: [
        { label:'収入', data:props.income, borderColor:#c026d3}
    ]
}
</script>
