<template>
    <div class="max-w-2xl mx-auto p-4">
        <h2 class="text-xl font-bold mb-4">2025年の給与一覧</h2>

        <!-- 合計部分 -->
        <div class="bg-blue-100 p-4 rounded mb-4 grid grid-cols-3 text-center">
            <div>
                <p class="text-gray-600">収入</p>
                <p class="text-lg font-bold text-blue-600">{{ totalIncome.toLocaleString() }}</p>
            </div>
            <div>
                <p class="text-gray-600">控除</p>
                <p class="text-lg font-bold text-red-600">{{ totalDeduction.toLocaleString() }}</p>
            </div>
            <div>
                <p class="text-gray-600">手取り</p>
                <p class="text-lg font-bold"> {{ netIncome.toLocaleString() }}</p>
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
    co
</script>
