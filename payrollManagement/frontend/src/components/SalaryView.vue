
<script setup>
import { defineProps, onMounted, ref, computed } from 'vue'
import { RouterLink, useLink } from 'vue-router'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Section from './Section.vue'

const props = defineProps({
    year: { type: Number, required: true },
    month: { type: String, required: true }
})

const router = useRouter()
const year = computed(() => props.year)

function goBack () {
    router.push({ path: '/', query: { year: props.year }})
}

const blankDetail = {
    id:        null,
    company:   '',
    base_salary: 0,  overtime_pay: 0,  allowances: 0,  transport: 0,
    expense_reimburse: 0,  income_other: 0,
    health_insurance: 0,   pension: 0,  employment_insurance: 0,
    nursing_insurance: 0, income_tax: 0,  resident_tax: 0,  deduction_other: 0,  refund: 0,
    working_days: 0, paid_leave: 0, working_hours: 0,
    overtime_in: '', overtime_out: '', holiday_work: '',
    memo: '',
    year: props.year,
    month: props.month
}

const detail = ref(null)
const isError = ref(false)

onMounted(async () => {
  try {
    const { data } = await axios.get(
      `/api/salaries/${props.year}/${encodeURIComponent(props.month)}`
    )
    detail.value = data[0] ?? { ...blankDetail }
  } catch (e) {
    isError.value = true
    console.error('明細取得失敗', e)
  }
})

const fmt = v => typeof v === 'number' ? v.toLocaleString() + ' 円' : v

function num(v){
    if (typeof v === 'number') return v
    const n = Number(String(v).replace(/[^\d.-]/g, ''))
    return isNaN(n) ? 0 : n
}

const incomeDetailRows = computed(() => detail.value ? [
  ['基本給',              detail.value.base_salary],
  ['時間外勤務',          detail.value.overtime_pay],
  ['各種手当',            detail.value.allowances],
  ['交通費（非課税）',    detail.value.transport],
  ['立替経費（非課税）',  detail.value.expense_reimburse],
  ['その他収入',          detail.value.income_other],
] : [])

const taxableTotal = computed(() =>
    num(detail.value?.base_salary) + num(detail.value?.overtime_pay) +
    num(detail.value?.allowances) + num(detail.value?.income_other))

const taxableRows = computed(() => [['課税対象収入', fmt(taxableTotal.value)]])

const deductDetailRows = computed(() => detail.value ? [
  ['健康保険料',    detail.value.health_insurance],
  ['厚生年金保険料',detail.value.pension],
  ['雇用保険料',    detail.value.employment_insurance],
  ['介護保険料',    detail.value.nursing_insurance],
  ['所得税',        detail.value.income_tax],
  ['住民税',        detail.value.resident_tax],
  ['その他控除',    detail.value.deduction_other],
  ['還付金',        -detail.value.refund],
] : [])

const incomeTotal = computed(() =>
    incomeDetailRows.value.reduce((s, [,v]) => s + num(v), 0))
const deductTotal = computed(() =>
    deductDetailRows.value.reduce((s, [,v]) => s + num(v), 0))

const incomeRows = computed(() =>
    incomeDetailRows.value.map(([l,v]) => [l, fmt(v)])
        .concat([['合計', fmt(incomeTotal.value)]]))

const deductRows = computed(() =>
    deductDetailRows.value.map(([l,v]) => [l, fmt(v)])
        .concat([['合計', fmt(deductTotal.value)]]))

const workRows = computed(() => detail.value ? [
  ['勤務日数',   detail.value.working_days],
  ['有給休暇',   detail.value.paid_leave],
  ['就労時間',   detail.value.working_hours],
  ['法定内残業', detail.value.overtime_in],
  ['法定外残業', detail.value.overtime_out],
  ['休日出勤',   detail.value.holiday_work],
] : [])

const otherRows = computed(() => [['—', '']])
const memoRows = computed(() => [[detail.value?.memo || '—', '']])

const netRows = computed(() => [[
    '差引支給額',
    fmt(incomeTotal.value - deductTotal.value)
]])

async function onDelete () {
    if (!confirm('本当に削除しますか？')) return

    try {
        await axios.delete(`/api/salaries/${detail.value.id}`)
        alert('削除しました')
        await router.push({ path: '/', query: { year: props.year } })
    } catch (e) {
        alert('削除に失敗しました')
        console.error(e)
    }
}
</script>

<template>
  <div v-if="detail">
    <!-- Top bar: back + actions -->
    <div class="flex items-center justify-between mb-6">
      <button
        @click="goBack"
        class="text-sm text-gray-500 hover:text-gray-800 flex items-center gap-1"
      >
        &#8592; {{ year }}年へ戻る
      </button>
      <div class="flex gap-2">
        <router-link
          v-if="detail.id"
          :to="{ name: 'salary-edit', params: { id: detail.id } }"
          class="bg-blue-600 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          編集
        </router-link>
        <router-link
          v-else
          :to="{ path: '/salary/new', query: { year: props.year, month: props.month } }"
          class="bg-blue-600 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          新規入力
        </router-link>
        <button
          v-if="detail?.id"
          @click="onDelete"
          class="bg-red-500 text-white text-sm px-4 py-2 rounded-lg hover:bg-red-600"
        >
          削除
        </button>
      </div>
    </div>

    <!-- Title -->
    <h2 class="text-2xl font-bold text-gray-800 mb-1">
      {{ props.year }}年 {{ props.month }} 明細
    </h2>
    <p class="text-sm text-gray-500 mb-6">{{ detail.company }}</p>

    <!-- Detail Sections -->
    <div class="grid grid-cols-1 mb-5 md:grid-cols-3 gap-4 mx-auto items-stretch">
      <Section title="勤怠" :rows="workRows" />
      <Section title="支給" :rows="incomeRows" />
      <Section title="控除" :rows="deductRows" />
      <Section title="課税対象" :rows="taxableRows" />
      <Section title="差引合計" :rows="netRows" outerClass="md:col-span-2" />
      <Section title="メモ" :rows="memoRows" outerClass="md:col-span-3" />
    </div>
  </div>

  <p v-else-if="isError" class="text-red-500">データの取得に失敗しました</p>
  <p v-else class="text-gray-400">読み込み中...</p>
</template>
