<template>
  <router-view />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import YearlySummary from './components/YearlySummary.vue'
import SalaryForm from './components/SalaryForm.vue'

const year = new Date().getFullYear()
const selectedMonth =  ref('')
const isFormOpen = ref(false)

function openForm(month) {
  selectedMonth.value = month
  isFormOpen.value =true
}
</script>