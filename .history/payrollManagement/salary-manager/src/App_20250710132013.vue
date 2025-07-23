<template>
  <div id="app" class="p-4">
    <SalaryForm />
  </div>
  <div>

  <YearlySummary />
  </div>
</template>

<script setup>
import SalaryForm from './components/SalaryForm.vue'
import YearSummary from './components/YearlySummary.vue'
</script>