<template>
    <div class="p-6">
        <div class="flex items-center mb-4 gap-2">
            <button @click="changeYear(-1)" class="text-xl px-2 py-1 hover:bg-gray-200 rounded">
                ◀️
            </button>
        </div>
        <h2 class="text-2xl font-bold mb-4 text-center">
            {{ currentYear }}年の給与
        </h2>
        <div class="flex items-center mb-4 gap-2">
            <button @click="changeYear(+1)" class="text-xl px-2 py-1 hover:bg-gray-200 rounded">
                ▶️
            </button>
        </div>

        <!-- 合計部分 -->
        <div class="flex flex-wrap justify-center gap-6">
                <div class="bg-white shadow-md rounded-lg p-6 w-64 text-center">
                    <p class="text-gray-500">総額収入</p>
                    <p class="text-2xl font-bold text-blue-600">{{ totalIncome.toLocaleString() }}</p>
                </div>
                <div class="bg-white shadow-md rounded-lg p-6 w-64 text-center">
                    <p class="text-gray-500">総額控除</p>
                    <p class="text-2xl font-bold text-red-600">{{ totalDeduction.toLocaleString() }}</p>
                </div>
                <div class="bg-white shadow-md rounded-lg p-6 w-64 text-center">
                    <p class="text-gray-500">総額手取</p>
                    <p class="text-2xl font-bold text-green-600"> {{ netIncome.toLocaleString() }}</p>
                </div>
        </div>

        <!-- 月別一覧 -->
        <table class="w-full table-auto border-collapse">
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
                    <td class="border p-2">{{ (row.income - row.deduction).toLocaleString() }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
    import { ref, watch } from 'vue'
    import { useRoute, useRouter } from 'vue-router'
    import axios from 'axios'

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
    )

    async function loadYearData () {
        try {
            // `?year=` でフィルタして その年だけ取得
            const { data: raw } = await axios.get('/api/salaries', {
                params: { year: currentYear.value }
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
        } catch (err) {
            console.error('年データ取得失敗', err)
        }
    }

    watch(currentYear, loadYearData, { immediate:true })

    function changeYear(delta){ currentYear.value += delta }
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
