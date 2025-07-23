<script setup>
import { ref, onMounted } from 'vue'
import { Line } from 'vue-chartjs'
import YearLineChart from './YearLineChart.vue';
import axios from 'axios';
import { onMounted } from 'vue';

const rows = ref([]);
const loading = ref(true);
const error = ref('');
const axios = require('axios').defaults;

async function getIncomeByYear() {
    try {
        const response = await axios.get({ year });
        console.log(response);
    }catch (error) {
        console.log(error)
    } finally { loading.value = false }
}

export default {
    setup() {
        const count
    }
}


</script>

<template>
    <h2>Loading...</h2>
    <!-- <YearLineChart
        :labels = "labels"
        :income="incomes"
        :deduction="deductions"
        :net="nets"
        class="my-6"
    /> -->
</template>


