<template>
  <div class="border p-6 rounded shadow-md bg-white max-w-2xl mx-auto">
    <h3 class="text-xl font-bold mb-4 text-center">
      {{ year }}年 {{ month }}の給与入力
    </h3>

    <!-- 入力フォーム -->
    <form @submit.prevent="submitForm" class="text-flex">
      <!-- 会社名 -->
      <div class="flex items-center gap-4 mr-10">
        <label class="block w-20 shrink-0 text-sm mb-1">会社名</label>
        <input v-model="form.company" type="text" class="input flex-1 rounded px-2 py-1 min-w-0 bg-gray-300" required />
      </div>

      <h2 class="text-blue-600 mt-5">支給</h2>

      <div class="flex items-center gap-4 mt-5 mr-10">
        <label class="block w-20 shrink-0 text-sm mb-1">基本給</label>
        <input v-model.number="form.base_salary" type="number" class="input flex-1 rounded px-2 py-1 bg-gray-300" />
      </div>

      <div class="flex items-center gap-4 mt-5 mr-10">
        <label class="block w-20 shrink-0 text-sm mb-1">時間外勤務</label>
        <input v-model.number="form.overtime_pay" type="number" class="input flex-1 rounded px-2 py-1 bg-gray-300" />
      </div>

      <div class="flex items-center gap-4 mt-5 mr-10">
        <label class="block w-20 shrink-0 text-sm mb-1">各種手当</label>
        <input v-model.number="form.allowances" type="number" class="input flex-1 rounded px-2 py-1 bg-gray-300" />
      </div>

      <div class="flex items-center gap-4 mt-5 mr-10">
        <label class="block w-20 shrink-0 text-sm mb-1">交通費</label>
        <input v-model.number="form.transport" type="number" class="input flex-1 rounded px-2 py-1 bg-gray-300" />
      </div>

      <div class="flex items-center gap-4 mt-5 mr-10">
        <label class="block w-20 shrink-0 text-sm mb-1">立替経費</label>
        <input v-model.number="form.expense_reimburse" type="number" class="input flex-1 rounded px-2 py-1 bg-gray-300" />
      </div>

      <div class="flex items-center gap-4 mt-5 mr-10">
        <label class="block w-20 shrink-0 text-sm mb-1">その他収入</label>
        <input v-model.number="form.income_other" type="number" class="input flex-1 rounded px-2 py-1 bg-gray-300" />
      </div>

      <h2 class=" text-red-600 mt-5">控除</h2>
      <div class="flex items-center gap-4 mt-5 mr-10">
        <label class="block w-20 shrink-0 text-sm mb-1">健康保険料</label>
        <input v-model.number="form.health_insurance" type="number" class="input flex-1 rounded px-2 py-1 bg-gray-300" />
      </div>

      <div class="flex items-center gap-4 mt-5 mr-10">
        <label class="block w-20 shrink-0 text-sm mb-1">厚生年金保険料</label>
        <input v-model.number="form.pension" type="number" class="input flex-1 rounded px-2 py-1 bg-gray-300" />
      </div>

      <div class="flex items-center gap-4 mt-5 mr-10">
        <label class="block w-20 shrink-0 text-sm mb-1">雇用保険料</label>
        <input v-model.number="form.employment_insurance" type="number" class="input flex-1 rounded px-2 py-1 bg-gray-300" />
      </div>

      <div class="flex items-center gap-4 mt-5 mr-10">
        <label class="block w-20 shrink-0 text-sm mb-1">介護保険料</label>
        <input v-model.number="form.nursing_insurance" type="number" class="input flex-1 rounded px-2 py-1 bg-gray-300" />
      </div>

      <div class="flex items-center gap-4 mt-5 mr-10">
        <label class="block w-20 shrink-0 text-sm mb-1">所得税</label>
        <input v-model.number="form.income_tax" type="number" class="input flex-1 rounded px-2 py-1 bg-gray-300" />
      </div>

      <div class="flex items-center gap-4 mt-5 mr-10">
        <label class="block w-20 shrink-0 text-sm mb-1">住民税</label>
        <input v-model.number="form.resident_tax" type="number" class="input flex-1 rounded px-2 py-1 bg-gray-300" />
      </div>

      <div class="flex items-center gap-4 mt-5 mr-10">
        <label class="block w-20 shrink-0 text-sm mb-1">その他控除</label>
        <input v-model.number="form.deduction_other" type="number" class="input flex-1 rounded px-2 py-1 bg-gray-300" />
      </div>

      <div class="flex items-center gap-4 mt-5 mr-10">
        <label class="block w-20 shrink-0 text-sm mb-1">還付金</label>
        <input v-model.number="form.refund" type="number" class="input flex-1 rounded px-2 py-1 bg-gray-300" />
      </div>

      <h2 class="text-green-600 mt-5">勤怠</h2>

      <div class="flex items-center gap-4 mt-5 mr-10">
        <label class="block w-20 shrink-0 text-sm mb-1">勤務日数</label>
        <input v-model.number="form.working_days" type="number" class="input flex-1 rounded px-2 py-1 bg-gray-300" />
      </div>

      <div class="flex items-center gap-4 mt-5 mr-10">
        <label class="block w-20 shrink-0 text-sm mb-1">有給休暇</label>
        <input v-model.number="form.paid_leave" type="number" class="input flex-1 rounded px-2 py-1 bg-gray-300" />
      </div>

      <div class="flex items-center gap-4 mt-5 mr-10">
        <label class="block w-20 shrink-0 text-sm mb-1">就労時間</label>
        <input v-model.number="form.working_hours" type="number" class="input flex-1 rounded px-2 py-1 bg-gray-300" />
      </div>

      <div class="flex items-center gap-4 mt-5 mr-10">
        <label class="block w-20 shrink-0 text-sm mb-1">法定内残業</label>
        <input v-model="form.overtime_in" type="text" class="input flex-1 rounded px-2 py-1 bg-gray-300" />
      </div>

      <div class="flex items-center gap-4 mt-5 mr-10">
        <label class="block w-20 shrink-0 text-sm mb-1">法定外残業</label>
        <input v-model="form.overtime_out" type="text" class="input flex-1 rounded px-2 py-1 bg-gray-300" />
      </div>

      <div class="flex items-center gap-4 mt-5 mr-10">
        <label class="block w-20 shrink-0 text-sm mb-1">休日出勤</label>
        <input v-model="form.holiday_work" type="text" class="input flex-1 rounded px-2 py-1 bg-gray-300" />
      </div>

      <!-- ───── メモ ───── -->
      <div class="flex items-center gap-4 mt-10 mr-10">
        <label class="block w-20 shrink-0 text-sm mb-1">メモ</label>
        <textarea v-model="form.memo" rows="3" class="input flex-1 rounded px-2 py-1 bg-gray-300"></textarea>
      </div>

      <!-- ボタン -->
      <div class="flex justify-end gap-3 pt-4">
        <button type="button" @click="$router.back()" class="text-sm text-gray-500">
          閉じる
        </button>
        <button type="submit" class="bg-blue-600 text-white px-4 py-1 rounded">
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

/* ---------- ルーティング情報 ---------- */
const route  = useRoute()
const router = useRouter()
const id = route.params.id               // 文字列 (存在しなければ undefined)

/* ---------- 初期値 ---------- */
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

/* ---------- 既存データの読み込み ---------- */
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

/* ---------- 見出し用 ---------- */
const year  = computed(() => form.year)
const month = computed(() => form.month)

/* ---------- 送信 ---------- */
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
