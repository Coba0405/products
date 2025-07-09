<template>
    <form @submit.prevent="submitForm">
        <h2 class="text-xl font-bold mb-4">給与明細　登録フォーム</h2>

        <div class="mb-2">
            <label>年: <input v-model="form.year" type="number" min="2000" max="2099" required /></label>
        </div>

        <div class="mb-2">
            <label>月:
                <selsect v-model ="form.month" required>
                    <option v-for="m in months" :key="m" :value0"m">{{ m }}</option>
                </selsect>
            </label>
        </div>

        <div class="mb-2">
            <label>会社名: <input v-model="form.company" type="text" required /></label>
        </div>

        <div class="mb-2">
            <label>基本給: <input v-model.number="form.base_salary" type="number" /></label>
        </div>

        <div class="mb-2">
            <label>時間外勤務: <input v-model.number="form.overtime_pay" type="number" /></label>
        </div>
        <button type="submit" class="bg-blue-500 text-white px-4 py-1 rounded">登録</button>
    </form>
</template>

<script setup>
import { reactive } from 'vue'
import axios from 'axios'

const months = ['01','02','03','04','05','06','07','08','09','10','11','12', '夏季賞与', '冬季賞与', '特別賞与']

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
