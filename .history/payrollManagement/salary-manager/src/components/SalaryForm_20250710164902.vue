<template>
  <div></div>
    <div>
      <h2 class="text-xl font-bold mb-4">月を選択してください</h2>
      <div class="mb-4 flex flex-col gap-2 items-start">
        <button
          v-for="m in months"
          :key = "m"
          @click="selectMonth(m)"
          class="px-3 py-1 border rounded bg-yellow-100 hover:bg-blue-200 w-full text-left"
        >
          {{ m }}
        </button>
      </div>
      <form @submit.prevent="submitForm">
        <div v-if="isMonthSelected">
          <div class="mb-2">
              <label>会社名: <input v-model="form.company" type="text" required /></label>
          </div>

          <div class="mb-2">
              <label>基本給: <input v-model.number="form.base_salary" type="number" /></label>
          </div>

          <div class="mb-2">
              <label>時間外勤務: <input v-model.number="form.overtime_pay" type="number" /></label>
          </div>

          <div class="mb-2">
              <label>休日出勤: <input v-model.number="form.holiday_work" type="number" /></label>
          </div>

          <!-- 他の項目も後ほどここに追加 -->

          <button type="submit" class="bg-blue-500 text-white px-4 py-1 rounded">登録</button>
        </div>
      </form>
    </div>
</template>

<script setup>
import { reactive, ref, watch } from 'vue'
const isMonthSelected = ref((false))
import axios from 'axios'

const months = ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月', '夏季賞与', '冬季賞与', '特別賞与']

const form = reactive({
  year: new Date().getFullYear(),
  month: '',
  company: '',
  base_salary: 0,
  overtime_pay: 0,
  allowances: 0,
  transport: 0,
  expense_reimburse: 0,
  income_other: 0,
  health_insurance: 0,
  pension: 0,
  employment_insurance: 0,
  nursing_insurance: 0,
  social_insurance: 0,
  income_tax: 0,
  resident_tax: 0,
  deduction_other: 0,
  refund: 0,
  working_days: 0,
  paid_leave: 0,
  working_hours: 0,
  overtime_in: '',
  overtime_out: '',
  holiday_work: '',
  memo: ''
})

// monthが変化したら自動でisMonthSelectedをtrueにする
watch(() => form.month, (newVal) => {
  if (newVal) {
    isMonthSelected.value = true
  }
})

const submitForm = async () => {
  try {
    await axios.post('http://127.0.0.1:5000/api/salaries', form)
    alert('登録成功！')
  }
  catch (error) {
    alert('登録失敗')
    console.error(error)
  }
}
</script>

<style scoped>
form {
  max-width: 500px;
}
</style>
