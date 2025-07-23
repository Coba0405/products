<template>
  <div id="app" class="p-4">
    <YearlySummary @select-month="openForm" />
    <!-- フォームは月が選ばれた時だけ表示 -->
    <SalaryForm v-if="isFormOpen"
                :initial-year="year"
                :initial-month="selectMonth"
                @close="isFormOpen = false" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import YearlySummary from './components/YearlySummary.vue'
import SalaryForm from './components/SalaryForm.vue'

const year = new Date().getFullYear()
const selectedMonth =  ref('')
const isFormOpen ref(s)
</script>