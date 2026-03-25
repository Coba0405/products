<template>
  <div class="max-w-2xl mx-auto">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-bold text-gray-800">
        {{ form.year }}年 源泉徴収票の{{ id ? '編集' : '登録' }}
      </h2>
      <button type="button" @click="$router.back()" class="text-sm text-gray-400 hover:text-gray-600">
        ✕ 閉じる
      </button>
    </div>

    <form @submit.prevent="submitForm" class="space-y-6">
      <!-- 年・会社名 -->
      <div class="grid grid-cols-2 gap-4">
        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-gray-700">年</label>
          <input
            v-model.number="form.year"
            type="number"
            class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white"
            required
          />
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-gray-700">支払者名（会社名）</label>
          <input
            v-model="form.company"
            type="text"
            class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white"
          />
        </div>
      </div>

      <!-- 支払・所得 -->
      <div class="border border-blue-100 rounded-lg overflow-hidden">
        <div class="bg-blue-50 border-b border-blue-100 px-4 py-2">
          <h3 class="font-semibold text-blue-700">支払・所得</h3>
        </div>
        <div class="grid grid-cols-2 gap-4 p-4">
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">支払金額</label>
            <input v-model.number="form.payment_amount" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">給与所得控除後の金額</label>
            <input v-model.number="form.after_deduction" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">所得控除の額の合計額</label>
            <input v-model.number="form.total_income_deduction" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">源泉徴収税額</label>
            <input v-model.number="form.withholding_tax_amount" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
        </div>
      </div>

      <!-- 各種控除 -->
      <div class="border border-red-100 rounded-lg overflow-hidden">
        <div class="bg-red-50 border-b border-red-100 px-4 py-2">
          <h3 class="font-semibold text-red-600">各種控除</h3>
        </div>
        <div class="grid grid-cols-2 gap-4 p-4">
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">社会保険料等の金額</label>
            <input v-model.number="form.social_insurance_amount" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">生命保険料の控除額</label>
            <input v-model.number="form.life_insurance_deduction" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">地震保険料の控除額</label>
            <input v-model.number="form.earthquake_insurance_deduction" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">住宅借入金等特別控除の額</label>
            <input v-model.number="form.housing_loan_deduction" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">配偶者特別控除の額</label>
            <input v-model.number="form.spouse_deduction" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">扶養親族の数</label>
            <input v-model.number="form.dependent_count" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
        </div>
      </div>

      <!-- メモ -->
      <div class="flex flex-col gap-1">
        <label class="text-sm font-medium text-gray-700">メモ</label>
        <textarea
          v-model="form.memo"
          rows="3"
          class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white"
        ></textarea>
      </div>

      <!-- ボタン -->
      <div class="flex justify-end gap-3 pt-2">
        <button
          type="button"
          @click="$router.back()"
          class="px-4 py-2 text-sm border border-gray-300 rounded-lg text-gray-600 hover:bg-gray-50"
        >
          キャンセル
        </button>
        <button
          type="submit"
          class="px-6 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
        >
          {{ id ? '更新' : '登録' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const id = route.params.id ? Number(route.params.id) : null

const form = reactive({
  year: Number(route.query.year) || new Date().getFullYear(),
  company: '',
  payment_amount: 0,
  after_deduction: 0,
  total_income_deduction: 0,
  withholding_tax_amount: 0,
  social_insurance_amount: 0,
  life_insurance_deduction: 0,
  earthquake_insurance_deduction: 0,
  housing_loan_deduction: 0,
  spouse_deduction: 0,
  dependent_count: 0,
  memo: ''
})

onMounted(async () => {
  if (id) {
    const year = Number(route.query.year)
    const { data } = await axios.get(`/api/withholding_tax/${year}`)
    if (data) Object.assign(form, data)
  }
})

async function submitForm() {
  if (id) {
    await axios.put(`/api/withholding_tax/${id}`, form)
    alert('更新しました')
  } else {
    await axios.post('/api/withholding_tax', form)
    alert('登録しました')
  }
  router.push({ name: 'withholding-tax', params: { year: form.year } })
}
</script>
