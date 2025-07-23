<template>
    <YearLineChart
        :labels = "labels"
        

    />
</template>


<script setup>
import { Line } from 'vue-chartjs'
import YearLineChart from './YearLineChart.vue';
</script>
