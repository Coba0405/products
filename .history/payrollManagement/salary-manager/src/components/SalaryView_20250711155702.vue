<template>
    <div v-if="detail" class="p-6">
        <h2 class="text-3xl text-left font-bold mb-4">{{ props.year }}年 {{ props.month }} 月明細</h2>
        <p>会社名: {{ detail.company }}</p>

        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Section title="勤怠" :rows="workRows" />
            <Section title="支給" :rows="incomeRows" />
            <Section title="控除" :rows="deductRows" />
            <Section title="その他" :rows="otherRows" />
            <Section title="差引合計" :rows="netRows" outerClass="md:col-span-3" />
            <Section title="メモ" :rows="memoRows" />
        </div>
    </div>

    <p v-else-if="isError" class="text-red-500">データの取得に失敗しました</p>
    <p v-else>読み込み中...</p>
</template>

<script setup>
import { defineProps, onMounted, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import Section from './Section.vue'

const props = defineProps({
    year: String,
    month: String
})

const detail = ref(null)
const isError = ref(false)

// API呼び出し（階層　URL版）
onMounted(async () => {
    try {
        const { data } = await axios.get(`/api/salaries/${props.year}/${props.month}`)
        // res.dataは配列なので0要素目を取り出す
        detail.value = data[0] ?? null
    }
    catch (e) {
        isError.value = true
        console.error('明細取得失敗', e)
    }
})

const fmt = v => typeof v === 'number' ? v.toLocaleString() + ' 円' : v

// 数値抽出ヘルパー
function num(v){
    if (typeof v === 'number') ret
}

/* --- 行配列 --- */
const incomeDetailRows = computed(() => detail.value ? [
  ['基本給',        detail.value.base_salary],
  ['時間外勤務',    detail.value.overtime_pay],
  ['各種手当',      detail.value.allowances],
  ['交通費',        detail.value.transport],
  ['立替経費',      detail.value.expense_reimburse],
  ['その他収入',    detail.value.income_other],
] : [])

const deductDetailRows = computed(() => detail.value ? [
  ['健康保険料',    detail.value.health_insurance],
  ['厚生年金保険料',detail.value.pension],
  ['雇用保険料',    detail.value.employment_insurance],
  ['介護保険料',    detail.value.nursing_insurance],
  ['社会保険料',    detail.value.social_insurance],
  ['所得税',        detail.value.income_tax],
  ['住民税',        detail.value.resident_tax],
  ['その他控除',    detail.value.deduction_other],
  ['還付金',        -detail.value.refund],   // ー表記
] : [])

// 合計値
const incomeTotal = computed(() =>
    incomeDetailRows.value.reduce((s, [,v]) => s + num(v), 0))
const deductTotal = computed(() =>
    deductDetailRows.value.reduce((s, [,v]) => s + num(v), 0))

// 画面表示用（明細 + 合計行）
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

/* その他（今回:メモのみ空セル）*/
const otherRows = computed(() => [['—', '']])

/* メモ欄 */
const memoRows = computed(() => [[detail.value.memo || '—', '']])

/* 差引合計 */
const netRows = computed(() => [[
    '差引支給額',
    fmt(incomeTotal.value - deductTotal.value)
]])
</script>
