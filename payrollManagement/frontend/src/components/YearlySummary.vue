<template>
  <div>
    <!-- Year Navigation -->
    <div class="flex items-center justify-between mb-6 anim-fade-up">
      <button
        @click="changeYear(-1)"
        aria-label="前の年へ"
        class="w-10 h-10 flex items-center justify-center rounded-xl border border-slate-200 bg-white shadow-sm hover:border-blue-400 hover:text-blue-600 text-slate-500 text-lg transition-all active:scale-95"
      >
        &#8249;
      </button>
      <div class="flex flex-col items-center gap-0.5">
        <h2 class="text-2xl font-extrabold text-slate-900 tracking-tight tabular-nums">{{ currentYear }}<span class="text-base font-bold text-slate-400 ml-1">年の給与</span></h2>
        <router-link
          :to="{ name: 'withholding-tax', params: { year: currentYear } }"
          class="text-xs font-medium text-blue-600 hover:text-blue-500 transition-colors"
        >源泉徴収票を見る →</router-link>
      </div>
      <button
        @click="changeYear(+1)"
        aria-label="次の年へ"
        class="w-10 h-10 flex items-center justify-center rounded-xl border border-slate-200 bg-white shadow-sm hover:border-blue-400 hover:text-blue-600 text-slate-500 text-lg transition-all active:scale-95"
      >
        &#8250;
      </button>
    </div>

    <!-- Hero Panel：手取り＋チャートを一枚のダークパネルに -->
    <div
      class="relative rounded-3xl bg-gradient-to-br from-ink-800 via-ink-900 to-ink-950 shadow-hero p-6 md:p-8 mb-8 overflow-hidden anim-fade-up"
      style="animation-delay: 60ms"
    >
      <!-- 装飾グロー -->
      <div class="absolute -top-24 -right-24 w-72 h-72 rounded-full bg-blue-600/15 blur-3xl pointer-events-none"></div>
      <div class="absolute -bottom-32 -left-16 w-80 h-80 rounded-full bg-teal-500/10 blur-3xl pointer-events-none"></div>

      <div class="relative">
        <!-- 手取りヒーロー -->
        <div class="flex flex-col md:flex-row md:items-end md:justify-between gap-6 mb-7">
          <div>
            <p class="text-xs font-semibold text-teal-300/90 tracking-[0.2em] uppercase mb-2">Net Income ─ 総額手取</p>
            <p class="text-4xl md:text-5xl font-extrabold text-white tabular-nums tracking-tight leading-none">
              {{ animatedNet.toLocaleString() }}<span class="text-lg font-bold text-slate-400 ml-2">円</span>
            </p>

            <!-- 年収見込み（所得ベース） -->
            <div class="mt-4 flex items-center gap-2.5 flex-wrap">
              <span class="inline-flex items-center rounded-full bg-teal-400/10 ring-1 ring-teal-300/30 px-2.5 py-1">
                <span class="text-[10px] font-bold text-teal-300 tracking-[0.18em] uppercase">Estimated・見込</span>
              </span>
              <span class="text-sm font-medium text-slate-300">年収見込み（所得）</span>
              <span class="text-2xl md:text-3xl font-extrabold text-teal-200 tabular-nums tracking-tight leading-none">
                {{ animatedEstimate.toLocaleString() }}<span class="text-sm font-bold text-slate-500 ml-1">円</span>
              </span>
            </div>
            <p class="text-[11px] text-slate-500 mt-1.5 leading-relaxed">
              所得ベース（立替金・交通費を除く）／実績月の平均×12 ＋ 賞与
            </p>
          </div>
          <!-- サブ統計 -->
          <div class="flex gap-6 md:gap-8">
            <div>
              <p class="text-[11px] font-medium text-slate-400 mb-1">総額収入</p>
              <p class="text-lg font-bold text-blue-300 tabular-nums">{{ animatedIncome.toLocaleString() }}</p>
            </div>
            <div>
              <p class="text-[11px] font-medium text-slate-400 mb-1">総額控除</p>
              <p class="text-lg font-bold text-rose-300 tabular-nums">{{ animatedDeduction.toLocaleString() }}</p>
            </div>
            <div>
              <p class="text-[11px] font-medium text-slate-400 mb-1">課税対象収入</p>
              <p class="text-lg font-bold text-slate-200 tabular-nums">{{ animatedTaxable.toLocaleString() }}</p>
            </div>
          </div>
        </div>

        <!-- Chart -->
        <YearLineChart
          :labels="labels"
          :income="incomes"
          :deduction="deductions"
          :net="nets"
          class="w-full"
        />
      </div>
    </div>

    <!-- Monthly Table -->
    <div class="card anim-fade-up" style="animation-delay: 140ms">
      <table class="w-full text-sm">
        <thead>
          <tr class="text-left border-b border-slate-100">
            <th class="px-5 py-3.5 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">月</th>
            <th class="px-5 py-3.5 text-right text-[11px] font-semibold text-slate-400 uppercase tracking-wider">収入</th>
            <th class="px-5 py-3.5 text-right text-[11px] font-semibold text-slate-400 uppercase tracking-wider">控除</th>
            <th class="px-5 py-3.5 text-right text-[11px] font-semibold text-slate-400 uppercase tracking-wider">手取り</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(row, i) in monthlyData"
            :key="`${currentYear}-${row.month}`"
            :class="[
              'border-t border-slate-50 cursor-pointer transition-colors border-l-2 border-l-transparent anim-fade-up',
              row.income > 0 || row.deduction > 0
                ? 'hover:bg-blue-50/60 hover:border-l-blue-500'
                : 'text-slate-300 hover:bg-slate-50'
            ]"
            :style="{ animationDelay: `${180 + i * 30}ms` }"
            @click="$router.push({ path: `/salary/${currentYear}/${row.month}` })"
          >
            <td class="px-5 py-3 font-semibold text-slate-700">{{ row.month }}</td>
            <td class="px-5 py-3 text-right text-slate-600 tabular-nums">
              {{ row.income > 0 ? row.income.toLocaleString() : '—' }}
            </td>
            <td class="px-5 py-3 text-right text-rose-500/80 tabular-nums">
              {{ row.deduction > 0 ? row.deduction.toLocaleString() : '—' }}
            </td>
            <td class="px-5 py-3 text-right text-teal-700 font-bold tabular-nums">
              {{ row.income > 0 ? (row.income - row.deduction).toLocaleString() : '—' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import YearLineChart from './YearLineChart.vue'
import { useCountUp } from '../composables/useCountUp'

    const labels = ref([])
    const incomes = ref([])
    const deductions = ref([])
    const nets = ref([])

    const route = useRoute()
    const router = useRouter()
    const currentYear = ref(route.query.year ? Number(route.query.year) : new Date().getFullYear())

    const monthlyData = ref([])
    const totalIncome = ref(0)
    const totalDeduction = ref(0)
    const netIncome = ref(0)
    const totalTaxable = ref(0)
    const estimatedAnnualIncome = ref(0)   // 年収見込み（所得ベース）

    /* カウントアップ表示用 */
    const animatedNet = useCountUp(netIncome)
    const animatedIncome = useCountUp(totalIncome)
    const animatedDeduction = useCountUp(totalDeduction)
    const animatedTaxable = useCountUp(totalTaxable)
    const animatedEstimate = useCountUp(estimatedAnnualIncome)

    defineEmits(['select-month'])

    watch(
        () => route.query.year,
        (v) => {
            if (v) currentYear.value = Number(v)
        }
    )

    // null・空文字・undefined を 0 に正規化（数値カラムが空のレコードでも壊れないように）
    const n = v => Number(v) || 0

    async function loadYearData () {
        try {
            const { data: raw } = await axios.get('/api/salaries',
                { params:{ year: currentYear.value }
            })

            /* ─ 総計 ─ */
            totalIncome.value = raw.reduce(
            (s,r)=> s + n(r.base_salary) + n(r.overtime_pay) + n(r.allowances) + n(r.transport) +
                        n(r.expense_reimburse) + n(r.income_other) + n(r.lateness_deduction), 0)

            totalTaxable.value = raw.reduce(
            (s,r)=> s + n(r.base_salary) + n(r.overtime_pay) + n(r.allowances) + n(r.income_other) +
                        n(r.lateness_deduction), 0)

            totalDeduction.value = raw.reduce(
            (s,r)=> s + n(r.health_insurance) + n(r.pension) + n(r.employment_insurance) +
                        n(r.nursing_insurance) + n(r.child_care_support) + n(r.income_tax) +
                        n(r.resident_tax) + n(r.reimburse_deduction) + n(r.workation_fee) + n(r.deduction_other) - n(r.refund), 0)

            netIncome.value = totalIncome.value - totalDeduction.value

            /* ─ 年収見込み（所得ベース・立替金/交通費を除く） ─ */
            const REG_MONTH_EST = /^\d+月$/
            // 所得 = 基本給 + 残業 + 各種手当 + その他収入 + 遅早控除（交通費・立替金は除外）
            const taxableOf = r =>
                n(r.base_salary) + n(r.overtime_pay) + n(r.allowances) + n(r.income_other) +
                n(r.lateness_deduction)

            // 通常月（1〜12月）の所得を月ごとに集計（同月複数行も合算）
            const monthlyTaxable = {}
            raw.filter(r => REG_MONTH_EST.test(r.month)).forEach(r => {
                monthlyTaxable[r.month] = (monthlyTaxable[r.month] || 0) + taxableOf(r)
            })

            // 所得 > 0 の月だけを「実績月」とし、その平均を年換算
            const activeTaxables = Object.values(monthlyTaxable).filter(v => v > 0)
            const avgMonthlyTaxable = activeTaxables.length
                ? activeTaxables.reduce((s, v) => s + v, 0) / activeTaxables.length
                : 0

            // 賞与の所得（按分せずそのまま加算）
            const BONUS_MONTHS = ['夏季賞与', '冬季賞与', '特別賞与']
            const bonusTaxable = raw
                .filter(r => BONUS_MONTHS.includes(r.month))
                .reduce((s, r) => s + taxableOf(r), 0)

            estimatedAnnualIncome.value = Math.round(avgMonthlyTaxable * 12 + bonusTaxable)

            /* ─ 月別 ─ */
            const months = [
            '1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月',
            '夏季賞与','冬季賞与','特別賞与'
            ]

            monthlyData.value = months.map(m => {
            const rows = raw.filter(r => r.month === m)

            const income = rows.reduce(
                (s,r)=> s + n(r.base_salary) + n(r.overtime_pay) + n(r.allowances) + n(r.transport) +
                        n(r.expense_reimburse) + n(r.income_other) + n(r.lateness_deduction), 0)

            const deduction = rows.reduce(
                (s,r)=> s + n(r.health_insurance) + n(r.pension) + n(r.employment_insurance) +
                        n(r.nursing_insurance) + n(r.child_care_support) + n(r.income_tax) +
                        n(r.resident_tax) + n(r.reimburse_deduction) + n(r.workation_fee) + n(r.deduction_other) - n(r.refund), 0)

            return { month: m, income, deduction }
            })

            /* グラフ用データ */
            const REG_MONTH = /^\d+月$/
            const onlyMonthRows = monthlyData.value.filter(r => REG_MONTH.test(r.month))

            labels.value     = onlyMonthRows.map(r => r.month)
            incomes.value    = onlyMonthRows.map(r => +r.income)
            deductions.value = onlyMonthRows.map(r => +r.deduction)
            nets.value       = onlyMonthRows.map(r => +(r.income - r.deduction))
        } catch (err) {
            console.error('年データ取得失敗', err)
        }
    }

    watch(currentYear, loadYearData, { immediate:true })

    function changeYear(delta){
        currentYear.value += delta,
        router.replace({ path:'/', query:{ year: currentYear.value } })
    }

</script>
