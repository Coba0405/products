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
    labels: {}
})
</script>
