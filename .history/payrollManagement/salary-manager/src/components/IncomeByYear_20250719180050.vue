<template>
    <h2 aria-placeholder="">初期表示</h2>
    <!-- <YearLineChart
        :labels = "labels"
        :income="incomes"
        :deduction="deductions"
        :net="nets"
        class="my-6"
    /> -->
</template>


<script setup>
import { Line } from 'vue-chartjs'
// import flask from Flask
import YearLineChart from './YearLineChart.vue';
</script>
