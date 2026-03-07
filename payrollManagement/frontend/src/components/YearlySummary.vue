<template>
  <div>
    <!-- Year Navigation -->
    <div class="flex items-center justify-center gap-4 mb-6">
      <button
        @click="changeYear(-1)"
        class="w-9 h-9 flex items-center justify-center rounded-full border border-gray-300 hover:bg-gray-100 text-gray-600 text-lg font-bold"
      >
        &#8249;
      </button>
      <h2 class="text-2xl font-bold text-gray-800">{{ currentYear }}年の給与</h2>
      <button
        @click="changeYear(+1)"
        class="w-9 h-9 flex items-center justify-center rounded-full border border-gray-300 hover:bg-gray-100 text-gray-600 text-lg font-bold"
      >
        &#8250;
      </button>
    </div>

    <!-- Chart -->
    <YearLineChart
      :labels="labels"
      :income="incomes"
      :deduction="deductions"
      :net="nets"
      class="mb-8 w-full max-w-2xl mx-auto"
    />

    <!-- Summary Cards -->
    <div class="flex flex-wrap justify-center gap-4 mb-8">
      <div class="bg-white shadow rounded-lg p-5 w-52 text-center">
        <p class="text-sm text-gray-500 mb-1">総額収入</p>
        <p class="text-xl font-bold text-blue-600">{{ totalIncome.toLocaleString() }} 円</p>
      </div>
      <div class="bg-white shadow rounded-lg p-5 w-52 text-center">
        <p class="text-sm text-gray-500 mb-1">総額控除</p>
        <p class="text-xl font-bold text-red-500">{{ totalDeduction.toLocaleString() }} 円</p>
      </div>
      <div class="bg-white shadow rounded-lg p-5 w-52 text-center">
        <p class="text-sm text-gray-500 mb-1">総額手取</p>
        <p class="text-xl font-bold text-green-600">{{ netIncome.toLocaleString() }} 円</p>
      </div>
    </div>

    <!-- Monthly Table -->
    <div class="max-w-2xl mx-auto bg-white shadow rounded-lg overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr class="bg-gray-100 text-gray-600 text-left">
            <th class="px-5 py-3">月</th>
            <th class="px-5 py-3 text-right">収入</th>
            <th class="px-5 py-3 text-right">控除</th>
            <th class="px-5 py-3 text-right">手取り</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="row in monthlyData"
            :key="row.month"
            :class="[
              'border-t cursor-pointer transition-colors',
              row.income > 0 || row.deduction > 0
                ? 'hover:bg-blue-50'
                : 'text-gray-300 hover:bg-gray-50'
            ]"
            @click="$router.push({ path: `/salary/${currentYear}/${row.month}` })"
          >
            <td class="px-5 py-3 font-medium">{{ row.month }}</td>
            <td class="px-5 py-3 text-right text-blue-600">
              {{ row.income > 0 ? row.income.toLocaleString() : '—' }}
            </td>
            <td class="px-5 py-3 text-right text-red-500">
              {{ row.deduction > 0 ? row.deduction.toLocaleString() : '—' }}
            </td>
            <td class="px-5 py-3 text-right text-green-600">
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

    defineEmits(['select-month'])

    watch(
        () => route.query.year,
        (v) => {
            if (v) currentYear.value = Number(v)
        }
    )

    async function loadYearData () {
        try {
            const { data: raw } = await axios.get('/api/salaries',
                { params:{ year: currentYear.value }
            })

            /* ─ 総計 ─ */
            totalIncome.value = raw.reduce(
            (s,r)=> s + r.base_salary + r.overtime_pay + r.allowances + r.transport +
                        r.expense_reimburse + r.income_other, 0)

            totalDeduction.value = raw.reduce(
            (s,r)=> s + r.health_insurance + r.pension + r.employment_insurance +
                        r.nursing_insurance + r.social_insurance + r.income_tax +
                        r.resident_tax + r.deduction_other - r.refund, 0)

            netIncome.value = totalIncome.value - totalDeduction.value

            /* ─ 月別 ─ */
            const months = [
            '1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月',
            '夏季賞与','冬季賞与','特別賞与'
            ]

            monthlyData.value = months.map(m => {
            const rows = raw.filter(r => r.month === m)

            const income = rows.reduce(
                (s,r)=> s + r.base_salary + r.overtime_pay + r.allowances + r.transport +
                        r.expense_reimburse + r.income_other, 0)

            const deduction = rows.reduce(
                (s,r)=> s + r.health_insurance + r.pension + r.employment_insurance +
                        r.nursing_insurance + r.social_insurance + r.income_tax +
                        r.resident_tax + r.deduction_other - r.refund, 0)

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

<script>
export default {
    name: 'TotalCard',
    props:{ label:String, value:Number, color:String },
    template:`
        <div class="bg-white shadow-md rounded-lg p-6 w-64 text-center">
        <p class="text-gray-500">{{ label }}</p>
        <p :class="'text-2xl font-bold text-' + color + '-600'">
            {{ value.toLocaleString() }}
        </p>
        </div>
    `
}
</script>
