<template>
    <div class="p-6">
        <h2 class="text-2xl font-bold mb-4 text-center">{{ year }}年の給与一覧</h2>

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
                    @click="$router.push({ path: `/salary/${year}/${row.month}` })">
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

    const year = new Date().getFullYear()
    const monthlyData = ref([])
    const totalIncome = ref(0)
    const totalDeduction = ref(0)
    const netIncome = ref(0)

    defineEmits(['select-month'])

    onMounted(async () => {
        try {
            const { data: raw } =await axios.get(`/api/salaries/${ year }`)

            totalIncome.value = raw.reduce((s,r)=>
            s + r.base_salary + r.overtime_pay + r.allowances + r.transport +
                r.expense_reimburse + r.income_other , 0)

            totalDeduction.value = raw.reduce((s,r)=>
            s + r.health_insurance + r.pension + r.employment_insurance +
                r.nursing_insurance + r.social_insurance + r.income_tax +
                r.resident_tax + r.deduction_other - r.refund , 0)

            netIncome.value = totalIncome.value - totalDeduction.value

            const months = ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月','夏季賞与','冬季賞与','特別賞与']
            const summary = []

            for (const m of months) {
                const rows = raw.filter(r => r.month === m)

                const income = rows.reduce((s,r)=>
                    s + r.base_salary + r.overtime_pay + r.allowances + r.transport +
                        r.expense_reimburse + r.income_other , 0)

                const deduction = rows.reduce((s,r)=>
                    s + r.health_insurance + r.pension + r.employment_insurance +
                        r.nursing_insurance + r.social_insurance + r.income_tax +
                        r.resident_tax + r.deduction_other - r.refund , 0)

                summary.push({ month: m, income, deduction })
            }


            monthlyData.value = summary
        } catch (err) {
            console.error("データの取得に失敗しました", err)
        }
    })
</script>
