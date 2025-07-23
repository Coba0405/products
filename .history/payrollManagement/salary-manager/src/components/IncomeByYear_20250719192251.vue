<script setup>
import { ref, onMounted } from 'vue'
import { Line } from 'vue-chartjs'
import YearLineChart from './YearLineChart.vue';
// API呼び出しライブラリ
import axios from 'axios';

const rows = ref([]);
// データ取得中かどうかを示すフラグをtrue(読み込み中)で初期化
const loading = ref(true);
// エラーメッセージ表示用の文字列状態を空文字で初期化
const error = ref('');

// 年次データをサーバーから非同期で取得する処理をまとめた関数の定義を開始
async function loadYearlySummary() {
    // データ取得次のローディグ状態を明示的にtrueにセット
    loading.value = true
    error.value = ''
    try {
        // バックエンドの現行ルート名に合わせる
        const { data } = await axios.get('/IncomeByYear')
        rows.value = [...data].sort((a, b) => a.year - b.year)
        console.log(data);
    }catch (error) {
        console.error(error)
        error.value = '年次データの取得に失敗しました'
    } finally {
        loading.value = false
    }
}

onMounted(loadYearlySummary)
</script>

<template>
    <div class="p-6 space-y-4">
        <h1 class="text-xl font-bold">年別取得（表表示フェーズ）</h1>
        <div v-if="loading" class="text-gray-500">Loading...</div>
        <div v-else-if="error" class="text-red-500">{{ error }}</div>
        <div v-else>
            <table class="w-full table-auto border-collapse text-sm">
                <thead>
                    <tr class="bg-gray-100">
                        <th class="border px-2 py-1">年</th>
                        <th class="border px-2 py-1">収入</th>
                        <th class="border px-2 py-1">控除</th>
                        <th class="border px-2 py-1">手取り</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="r in rows" :key="r.year" class="hover:bg-gray-50">
                        <td class="border px-2 py-1">{{ r.year }}</td>
                        <td class="border px-2 py-1 text-blue-600">{{ r.income.toLocaleString() }}</td>
                        <td class="border px-2 py-1 text-red-600">{{ r.deduction.toLocaleString() }}</td>
                        <td class="border px-2 py-1 text-green-600">{{ r.net.toLocaleString() }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    <!-- <YearLineChart
        :labels = "labels"
        :income="incomes"
        :deduction="deductions"
        :net="nets"
        class="my-6"
    /> -->
</template>


