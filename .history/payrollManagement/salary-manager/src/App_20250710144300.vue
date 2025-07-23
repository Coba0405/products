<template>
  <div id="app" class="p-4">
    <SalaryForm />
    <div class="text-center text-2xl text-blue-600">
    Tailwind CSSが使えています！
  </div>
    <YearlySummary />
  </div>
</template>

<script setup>
import SalaryForm from './components/SalaryForm.vue'
import YearlySummary from './components/YearlySummary.vue'
</script>