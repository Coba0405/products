<script setup>
import { ref, onMounted } from 'vue'
import { Line } from 'vue-chartjs'
import YearLineChart from './YearLineChart.vue';
import axios from 'axios';

const rows = ref([]);
const loading = ref(true);
const error = ref('');
const axios = require('axios').defaults;

async function loadYearlySummary() {
    loading.value = true
    error.value = ''
    try {
        // バックエンドの現行ルート名に合わせる
        const { data } = await axios.get('/IncomeByYear')
        // const response = await axios.get({ year });
        rows.value = [...data].sort((a, b) => a.year - b.year)
        console.log(data);
    }catch (error) {
        console.error(error)
        error.value = '年次データの取得に失敗しました'
    } finally {
        loading.value = false
    }
}

onMounted(loadYearlySummary)
</script>

<template>
    <div class="p-6 space-y-4">
    <h2>Loading...</h2>
        <h1></h1>
    </div>
    <!-- <YearLineChart
        :labels = "labels"
        :income="incomes"
        :deduction="deductions"
        :net="nets"
        class="my-6"
    /> -->
</template>


