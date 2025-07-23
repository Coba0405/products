<template>
  <div class="border p-6 rounded shadow-md bg-white max-w-lg mx-auto">
    <h3 class="text-xl font-hold mb-4 text-center">
      {{ form.year }}年 {{  form.month }}月の給与入力
    </h3>

    <!-- 入力フォーム本体 -->
    <form @submit.prevent="submitForm" class="space-y-3">
      <div>
        <label class="block text-sm mb-1">会社名</label>
        <input v-model.number="form.company" type="text" class="input" required />
      </div>
      
      <div>
        <label class="block text-sm mb-1">基本給</label>
        <input v-model.number="form.base_salary" type="number" class="input" />
      </div>

      <div>
        <label class="block text-sm mb-1">時間外勤務</label>
        <input v-model.number="form.overtime_pay" type="number" class="input" />
      </div>

      <div>
        <label class="block text-sm mb-1">休日出勤</label>
        <input v-model.number="form.overtime_pay" type="number" class="input" />
      </div>

      <!-- 他の項目も後ほどここに追加 -->
      
      <div class="flex justify-end gap-3 pt-4">
        <button type="button" @click="$emit('close')" class="text-sm text-gray-500">閉じる</button>
        <button type="submit" class="bg-blue-600 text-white px-4 py-1 rounded">登録</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import axios from 'axios'

// propsで年と年を受け取る
const props =defineProps

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
