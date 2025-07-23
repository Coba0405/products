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
        
        console.log(response);
    }catch (error) {
        console.log(error)
    } finally { loading.value = false }
}

export default {
    setup() {
        const count = ref(0)
        return {
            count
        }
    },
    mounted() {
        console.log(this.count)
    }
}
</script>

<template>
    <h2>Loading...</h2>
    <button @click="count++">{{ count }}</button>
    <!-- <YearLineChart
        :labels = "labels"
        :income="incomes"
        :deduction="deductions"
        :net="nets"
        class="my-6"
    /> -->
</template>


