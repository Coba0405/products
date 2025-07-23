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
                    <th class="bor"></th>
                </tr>
            </thead>
        </table>
    </div>
</template>

<script setup>

</script>
