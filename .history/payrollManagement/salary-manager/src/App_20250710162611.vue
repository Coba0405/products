<template>
  <div id="app" class="p-4">
    <YearlySummary @select-month="openForm" />
    <!-- フォームは月が選ばれた時だけ表示 -->
    <SalaryForm v-if="isFormOpen"
                :initial-y />
  </div>
</template>

<script setup>
import SalaryForm from './components/SalaryForm.vue'
import YearlySummary from './components/YearlySummary.vue'
</script>