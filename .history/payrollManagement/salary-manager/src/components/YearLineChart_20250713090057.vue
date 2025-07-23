<template>
    <!--  親要素の高さで可変にしたいなら h-64 とかを付ける  -->
    <Line :data="data" :options="optopns" class="w-full" h-64 />
</template>

<script setup>
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, LineElement, LinearScale, CategoryScale, Legend, Title, Tooltip } from 'chart.js'

// 使用するパーツだけ登録
ChartJS.register(LineE)
</script>
