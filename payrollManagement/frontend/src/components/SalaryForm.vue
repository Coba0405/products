<template>
  <div class="max-w-2xl mx-auto">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-bold text-gray-800">
        {{ year }}年{{ month ? ' ' + month : '' }} の給与入力
      </h2>
      <button type="button" @click="$router.back()" class="text-sm text-gray-400 hover:text-gray-600">
        ✕ 閉じる
      </button>
    </div>

    <form @submit.prevent="submitForm" class="space-y-6">
      <!-- 年・月 -->
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
          <label class="text-sm font-medium text-gray-700">月</label>
          <select
            v-model="form.month"
            class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white"
            required
          >
            <option value="" disabled>選択してください</option>
            <option v-for="m in months" :key="m" :value="m">{{ m }}</option>
          </select>
        </div>
      </div>

      <!-- 会社名 -->
      <div class="flex flex-col gap-1">
        <label class="text-sm font-medium text-gray-700">会社名</label>
        <input
          v-model="form.company"
          type="text"
          class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white"
          required
        />
      </div>

      <!-- 支給 -->
      <div class="border border-blue-100 rounded-lg overflow-hidden">
        <div class="bg-blue-50 border-b border-blue-100 px-4 py-2">
          <h3 class="font-semibold text-blue-700">支給</h3>
        </div>
        <div class="grid grid-cols-2 gap-4 p-4">
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">基本給</label>
            <input v-model.number="form.base_salary" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">時間外勤務</label>
            <input v-model.number="form.overtime_pay" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">各種手当</label>
            <input v-model.number="form.allowances" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">交通費</label>
            <input v-model.number="form.transport" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">立替経費</label>
            <input v-model.number="form.expense_reimburse" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">その他収入</label>
            <input v-model.number="form.income_other" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
        </div>
      </div>

      <!-- 控除 -->
      <div class="border border-red-100 rounded-lg overflow-hidden">
        <div class="bg-red-50 border-b border-red-100 px-4 py-2">
          <h3 class="font-semibold text-red-600">控除</h3>
        </div>
        <div class="grid grid-cols-2 gap-4 p-4">
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">健康保険料</label>
            <input v-model.number="form.health_insurance" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">厚生年金</label>
            <input v-model.number="form.pension" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">雇用保険料</label>
            <input v-model.number="form.employment_insurance" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">介護保険料</label>
            <input v-model.number="form.nursing_insurance" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">所得税</label>
            <input v-model.number="form.income_tax" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">住民税</label>
            <input v-model.number="form.resident_tax" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">その他控除</label>
            <input v-model.number="form.deduction_other" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">還付金</label>
            <input v-model.number="form.refund" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
        </div>
      </div>

      <!-- 勤怠 -->
      <div class="border border-green-100 rounded-lg overflow-hidden">
        <div class="bg-green-50 border-b border-green-100 px-4 py-2">
          <h3 class="font-semibold text-green-700">勤怠</h3>
        </div>
        <div class="grid grid-cols-2 gap-4 p-4">
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">勤務日数</label>
            <input v-model.number="form.working_days" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">有給休暇</label>
            <input v-model.number="form.paid_leave" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">就労時間</label>
            <input v-model.number="form.working_hours" type="number" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">法定内残業</label>
            <input v-model="form.overtime_in" type="text" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">法定外残業</label>
            <input v-model="form.overtime_out" type="text" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm text-gray-600">休日出勤</label>
            <input v-model="form.holiday_work" type="text" class="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-300 bg-white" />
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
import { reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route  = useRoute()
const router = useRouter()
const id = route.params.id

const months = [
  '1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月',
  '夏季賞与','冬季賞与','特別賞与'
]

const initialYear  = Number(route.query.year)  || new Date().getFullYear()
const initialMonth =       route.query.month   || ''

const form = reactive({
  year: initialYear,
  month: initialMonth,
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

onMounted(async () => {
  if (id) {
    const { data } = await axios.get(`/api/salaries/${id}`)
    if (data && data.id) {
      Object.assign(form, data)
    } else {
      alert('レコードが見つかりません（新規入力をします）')
    }
  }
})

const year  = computed(() => form.year)
const month = computed(() => form.month)

async function submitForm () {
  if (id) {
    await axios.put(`/api/salaries/${id}`, form)
    alert('更新しました')
  } else {
    await axios.post('/api/salaries', form)
    alert('登録しました')
  }
  router.back()
}
</script>
