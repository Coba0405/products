<template>
    <div class="max-w-2xl mx-auto p-4">
        <h2 class="text-xl font-bold mb-4">2025年の給与一覧</h2>

        <!-- 合計部分 -->
        <div class="w-full max-w-3xl mx-auto">
            <div class="d-flax flax-row justify-center">
                <div>
                    <p class="text-gray-600">総額収入</p>
                    <p class="text-lg font-bold text-blue-600">{{ totalIncome.toLocaleString() }}</p>
                </div>
                <div>
                    <p class="text-gray-600">総額控除</p>
                    <p class="text-lg font-bold text-red-600">{{ totalDeduction.toLocaleString() }}</p>
                </div>
                <div>
                    <p class="text-gray-600">総額手取</p>
                    <p class="text-lg font-bold"> {{ netIncome.toLocaleString() }}</p>
                </div>
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
                <tr v-for="row in monthlyData" :key="row.month">
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
    import { ref, onMounted } from 'vue'
    import axios from 'axios'

    const monthlyData = ref([])
    const totalIncome = ref(0)
    const totalDeduction = ref(0)
    const netIncome = ref(0)

    onMounted(async () => {
        try {
            const res =await axios.get('http://127.0.0.1:5000/api/salaries/2025')
            const raw = res.data

            const summary = []
            let incomeSum = 0
            let deductionSum = 0

            for (const m of ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月', '夏季賞与', '冬季賞与', '特別賞与']) {
                const rows = raw.filter(row => row.month === m)

                const income = rows.reduce((sum, r) =>
                    sum +
                    r.base_salary +
                    r.overtime_pay +
                    r.allowances +
                    r.transport +
                    r.expense_reimburse +
                    r.income_other, 0
                )

                const deduction = rows.reduce((sum, r) =>
                    sum +
                    r.health_insurance +
                    r.pension +
                    r.employment_insurance +
                    r.nursing_insurance +
                    r.social_insurance +
                    r.income_tax +
                    r.resident_tax +
                    r.deduction_other -
                    r.refund, 0
                )

                incomeSum += income
                deductionSum += deduction

                summary.push({
                    month: m,
                    income,
                    deduction
                })
            }

            monthlyData.value = summary
            totalIncome.value = incomeSum
            totalDeduction.value = deductionSum
            netIncome.value = incomeSum - deductionSum

        } catch (err) {
            console.error("データの取得に失敗しました", err)
        }
    })
</script>

<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold mb-4 text-center">年間サマリー（{{ year }}年）</h2>
    
    <div class="flex flex-wrap justify-center gap-6">
      <div class="bg-white shadow-md rounded-lg p-6 w-64 text-center">
        <p class="text-gray-500">総額収入</p>
        <p class="text-2xl font-bold text-blue-600">{{ totalIncome.toLocaleString() }} 円</p>
      </div>
      <div class="bg-white shadow-md rounded-lg p-6 w-64 text-center">
        <p class="text-gray-500">総額控除</p>
        <p class="text-2xl font-bold text-red-600">{{ totalDeduction.toLocaleString() }} 円</p>
      </div>
      <div class="bg-white shadow-md rounded-lg p-6 w-64 text-center">
        <p class="text-gray-500">総額手取</p>
        <p class="text-2xl font-bold text-green-600">{{ netIncome.toLocaleString() }} 円</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const year = new Date().getFullYear()
const totalIncome = ref(0)
const totalDeduction = ref(0)
const netIncome = ref(0)

onMounted(async () => {
  const res = await axios.get(`http://127.0.0.1:5000/api/salaries/${year}`)
  const data = res.data

  totalIncome.value = data.reduce((sum, row) =>
    sum + row.base_salary + row.overtime_pay + row.allowances + row.transport + row.expense_reimburse + row.income_other, 0)

  totalDeduction.value = data.reduce((sum, row) =>
    sum + row.health_insurance + row.pension + row.employment_insurance + row.nursing_insurance + row.social_insurance + row.income_tax + row.resident_tax + row.deduction_other - row.refund, 0)

  netIncome.value = totalIncome.value - totalDeduction.value
})
</script>
