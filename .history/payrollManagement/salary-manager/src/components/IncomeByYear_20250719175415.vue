<template>
    <YearLineChart
        :labels = "labels"
        :income="incomes"
        :deduction="deductions"
        :net="nets"
        class="my-6"
    />
</template>


<script setup>
import { Line } from 'vue-chartjs'
import Flask from
import YearLineChart from './YearLineChart.vue';
</script>
