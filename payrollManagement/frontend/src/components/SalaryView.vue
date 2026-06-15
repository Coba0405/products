
<script setup>
import { defineProps, onMounted, ref, computed } from 'vue'
import { RouterLink, useLink } from 'vue-router'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Section from './Section.vue'
import ToastNotification from './ToastNotification.vue'
import ConfirmDialog from './ConfirmDialog.vue'

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
    expense_reimburse: 0,  income_other: 0,  lateness_deduction: 0,
    health_insurance: 0,   pension: 0,  employment_insurance: 0,
    nursing_insurance: 0, child_care_support: 0, income_tax: 0,  resident_tax: 0,
    reimburse_deduction: 0, workation_fee: 0, deduction_other: 0,  refund: 0,
    working_days: 0, paid_leave: 0, working_hours: 0,
    overtime_in: '', overtime_out: '', holiday_work: '', late_early_time: '',
    memo: '',
    year: props.year,
    month: props.month
}

const detail = ref(null)
const isError = ref(false)
const toast = ref(null)
const confirmDialog = ref(null)

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
  ['立替経費（支給・非課税）', detail.value.expense_reimburse],
  ['遅早控除',            detail.value.lateness_deduction],
  ['その他収入',          detail.value.income_other],
] : [])

const taxableTotal = computed(() =>
    num(detail.value?.base_salary) + num(detail.value?.overtime_pay) +
    num(detail.value?.allowances) + num(detail.value?.income_other) +
    num(detail.value?.lateness_deduction))

const taxableRows = computed(() => [['課税対象収入', fmt(taxableTotal.value)]])

const deductDetailRows = computed(() => detail.value ? [
  ['健康保険料',      detail.value.health_insurance],
  ['子ども子育て支援金', detail.value.child_care_support],
  ['厚生年金保険料',  detail.value.pension],
  ['雇用保険料',      detail.value.employment_insurance],
  ['介護保険料',      detail.value.nursing_insurance],
  ['所得税',          detail.value.income_tax],
  ['住民税',          detail.value.resident_tax],
  ['当月立替経費',    detail.value.reimburse_deduction],
  ['ワーケーション費用', detail.value.workation_fee],
  ['その他控除',      detail.value.deduction_other],
  ['還付金',          -detail.value.refund],
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
  ['遅早時間',   detail.value.late_early_time],
  ['休日出勤',   detail.value.holiday_work],
] : [])

const otherRows = computed(() => [['—', '']])
const memoRows = computed(() => [[detail.value?.memo || '—', '']])

const netRows = computed(() => [[
    '差引支給額',
    fmt(incomeTotal.value - deductTotal.value)
]])

async function onDelete () {
    const ok = await confirmDialog.value?.open({
        title: '給与明細を削除しますか？',
        message: 'この操作は取り消せません。',
        confirmLabel: '削除',
        danger: true
    })
    if (!ok) return

    try {
        await axios.delete(`/api/salaries/${detail.value.id}`)
        toast.value?.show('削除しました', 'success')
        setTimeout(() => router.push({ path: '/', query: { year: props.year } }), 800)
    } catch (e) {
        toast.value?.show('削除に失敗しました', 'error')
        console.error(e)
    }
}
</script>

<template>
  <div>
  <div v-if="detail">
    <!-- Top bar: back + actions -->
    <div class="flex items-center justify-between mb-6 anim-fade-up">
      <button
        @click="goBack"
        class="text-sm font-medium text-slate-500 hover:text-slate-900 flex items-center gap-1.5 transition-colors group"
      >
        <span class="transition-transform group-hover:-translate-x-0.5">&#8592;</span> {{ year }}年へ戻る
      </button>
      <div class="flex gap-2">
        <router-link
          v-if="detail.id"
          :to="{ name: 'salary-edit', params: { id: detail.id } }"
          class="btn-primary !py-2"
        >
          編集
        </router-link>
        <router-link
          v-else
          :to="{ path: '/salary/new', query: { year: props.year, month: props.month } }"
          class="btn-primary !py-2"
        >
          新規入力
        </router-link>
        <button
          v-if="detail?.id"
          @click="onDelete"
          class="btn-danger !py-2"
        >
          削除
        </button>
      </div>
    </div>

    <!-- Title -->
    <h2 class="text-2xl font-extrabold text-slate-900 mb-1 tracking-tight anim-fade-up" style="animation-delay: 40ms">
      {{ props.year }}年 {{ props.month }} 明細
    </h2>
    <p class="text-sm text-slate-500 mb-6 anim-fade-up" style="animation-delay: 70ms">{{ detail.company }}</p>

    <!-- Detail Sections -->
    <div class="grid grid-cols-1 mb-5 md:grid-cols-3 gap-4 mx-auto items-stretch">
      <div class="anim-fade-up h-full" style="animation-delay: 100ms"><Section title="勤怠" :rows="workRows" /></div>
      <div class="anim-fade-up h-full" style="animation-delay: 150ms"><Section title="支給" :rows="incomeRows" /></div>
      <div class="anim-fade-up h-full" style="animation-delay: 200ms"><Section title="控除" :rows="deductRows" /></div>
      <div class="anim-fade-up h-full" style="animation-delay: 250ms"><Section title="課税対象" :rows="taxableRows" /></div>
      <div class="anim-fade-up h-full md:col-span-2" style="animation-delay: 300ms"><Section title="差引合計" :rows="netRows" /></div>
      <div class="anim-fade-up h-full md:col-span-3" style="animation-delay: 350ms"><Section title="メモ" :rows="memoRows" /></div>
    </div>
  </div>

  <p v-else-if="isError" class="text-rose-500">データの取得に失敗しました</p>
  <p v-else class="text-slate-400">読み込み中...</p>

  <ToastNotification ref="toast" />
  <ConfirmDialog ref="confirmDialog" />
  </div>
</template>
