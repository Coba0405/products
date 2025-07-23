<template>
  <div id="app" class="p-4">
    <YearlySummary @se/>
    <SalaryForm />
  </div>
</template>

<script setup>
import SalaryForm from './components/SalaryForm.vue'
import YearlySummary from './components/YearlySummary.vue'
</script>