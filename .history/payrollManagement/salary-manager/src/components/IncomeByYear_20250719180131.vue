<template>
    <h2><Loading class=""></Loading></h2>
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
