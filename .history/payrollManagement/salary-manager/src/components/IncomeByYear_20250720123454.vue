<script setup>
import { ref, onMounted, defineProps } from 'vue'
import { useRouter } from 'vue-router'
import YearLineChart from './YearLineChart.vue';
// API呼び出しライブラリ
import axios from 'axios';

// この子コンポーネントはyearという数字を必ずもらうと宣言
const props = defineProps({
    year: {type: Number, required: true},
})
console.log(props.year)

const router = useRouter()
const rows = ref([]);
// データ取得中かどうかを示すフラグをtrue(読み込み中)で初期化
const loading = ref(true);
// エラーメッセージ表示用の文字列状態を空文字で初期化
const errorMessage = ref('');

// 年次データをサーバーから非同期で取得する処理をまとめた関数の定義を開始
async function loadYearlySummary() {
    // データ取得次のローディグ状態を明示的にtrueにセット
    loading.value = true
    // 以前のエラーメッセージが残らないようエラー用の文字列リセット
    errorMessage.value = ''
    try {
        // エンドポイント/IncomeByYearにGETリクエストを送る→レスポンス(json)をdataに取り出すまで待機
        const { data } = await axios.get('/IncomeByYear')

        if (!Array.isArray(data)) {
            console.warn('Not array:', data)
            throw new Error('非配列レスポンス')
        }
        // dataをスプレッドで複製し、yearを昇順でソートしrowsに代入
        rows.value = data
            .filter(row => row && typeof row.year === 'number')
            .sort((a, b) => a.year - b.year)
    }catch (err) {
        console.error(err)
        errorMessage.value = '年次データの取得に失敗しました'
        // 成功・失敗とわず最後に必ず実行したい処理の開始
    } finally {
        // データ取得処理が終わったのでローディング状態を解除
        loading.value = false
    }
}
// @clickで呼ばれる関数
function goBack () {
    // '/'の後ろに　?year=XXXX をつけるようrouterに依頼
    // router.push({ path: '/', query: {year: props.year } }) historyを残す場合は.push
    router.replace({ path: '/', query: {year: props.year} }) //historyを残さない場合は.replace
}

// コンポーネントが画面にマウントされたタイミングでloadYearlySummaryを自動実行する
onMounted(loadYearlySummary)
</script>

<template>
    <div class="p-6 space-y-4">
        <h1 class="text-xl font-bold">年別取得（表表示フェーズ）</h1>
        <div v-if="loading" class="text-gray-500">Loading...</div>
        <div v-else-if="errorMessage" class="text-red-500">{{ errorMessage }}</div>
        <!-- ローディング、エラーのない(正常にデータがある)場合の表示ブロックを開始 -->
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
                    <!-- rowsの各要素を反復表示　年をkeyとして指定する -->
                    <tr v-for="row in rows" :key="row.year" class="hover:bg-gray-50">
                        <td class="border px-2 py-1">{{ row.year }}</td>
                        <td class="border px-2 py-1 text-blue-600">{{ row.income.toLocaleString() }}</td>
                        <td class="border px-2 py-1 text-red-600">{{ row.deduction.toLocaleString() }}</td>
                        <td class="border px-2 py-1 text-green-600">{{ row.net.toLocaleString() }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <button
        @click="goBack"
        class="mb-4 inline-flex items-center gap-1 text-blue-600 hover:underline"
        >
            <span>{{ props.year }}年へ戻る</span>
        </button>
        <!-- <YearLineChart
            :labels = "labels"
            :income="incomes"
            :deduction="deductions"
            :net="nets"
            class="my-6"
        /> -->
    </div>
</template>


