<template>
    <div class="p-6">
        <router-link
            :to="{ name: 'income-by-year', query: { year: currentYear } }"
            class="block px-4 py-2 hover:bg-gray-100 text-blue-600"
        >
            <strong>年別所得</strong>
        </router-link>
        <h2 class="text-2xl font-bold mb-4 text-center">
            <button @click="changeYear(-1)" class="text-xl px-2 py-1 hover:bg-gray-200 rounded">
                ◀️
            </button>
            {{ currentYear }}年の給与
            <button @click="changeYear(+1)" class="text-xl px-2 py-1 hover:bg-gray-200 rounded">
                ▶️
            </button>
        </h2>

        <YearLineChart
            :labels="labels"
            :income="incomes"
            :deduction="deductions"
            :net="nets"
            class="my-6 w-[45%] mx-auto"
        />

        <!-- 合計部分 -->
        <div class="flex flex-wrap justify-center gap-6">
            <div class="bg-white shadow-md rounded-lg p-6 w-64 m-8 text-center">
                <p class="text-gray-500">総額収入</p>
                <p class="text-2xl font-bold text-blue-600">{{ totalIncome.toLocaleString() }}</p>
            </div>
            <div class="bg-white shadow-md rounded-lg p-6 w-64 m-8 text-center">
                <p class="text-gray-500">総額控除</p>
                <p class="text-2xl font-bold text-red-600">{{ totalDeduction.toLocaleString() }}</p>
            </div>
            <div class="bg-white shadow-md rounded-lg p-6 w-64 m-8 text-center">
                <p class="text-gray-500">総額手取</p>
                <p class="text-2xl font-bold text-green-600"> {{ netIncome.toLocaleString() }}</p>
            </div>
        </div>

        <!-- 月別一覧 -->
        <table class="w-[] table-auto border-collapse">
            <thead>
                <tr class="bg-gray-200">
                    <th class="border p-2">月</th>
                    <th class="border p-2">収入</th>
                    <th class="border p-2">控除</th>
                    <th class="border p-2">手取り</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="row in monthlyData"
                    :key="row.month"
                    class="hover:bg-gray-100 cursor-pointer"
                    @click="$router.push({ path: `/salary/${currentYear}/${row.month}` })">
                    <td class="border p-2">{{ row.month }}</td>
                    <td class="border p-2 text-blue-600">{{ row.income.toLocaleString() }}</td>
                    <td class="border p-2 text-red-600">{{ row.deduction.toLocaleString() }}</td>
                    <td class="border p-2 text-green-600">{{ (row.income - row.deduction).toLocaleString() }}</td>
                </tr>
            </tbody>
        </table>
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
            // `?year=` でフィルタして その年だけ取得
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

            /* ====▼ 追加：グラフ用データを別に組み立てる ========= */
            const REG_MONTH = /^\d+月$/                 // 1〜12月だけマッチ
            const onlyMonthRows = monthlyData.value.filter(r => REG_MONTH.test(r.month))

            // グラフ用ラベルと数値配列
            labels.value     = onlyMonthRows.map(r => r.month)
            incomes.value  = onlyMonthRows.map(r => +r.income)
            deductions.value  = onlyMonthRows.map(r => +r.deduction)
            nets.value     = onlyMonthRows.map(r => +(r.income - r.deduction))
        } catch (err) {
            console.error('年データ取得失敗', err)
        }

        // console.log('labels', labels.value)
        // console.log('incomes', incomes.value)
        // console.log('deductions', deductions.value)
        // console.log('nets', nets.value)
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
