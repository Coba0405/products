<script setup>
import { ref, onMounted, defineProps, computed } from 'vue'
import { useRouter } from 'vue-router'
import YearLineChart from './YearLineChart.vue';
import axios from 'axios';

const props = defineProps({
    year: {type: Number, required: true},
})

const router = useRouter()
const rows = ref([]);
const loading = ref(true);
const errorMessage = ref('');

async function loadYearlySummary() {
    loading.value = true
    errorMessage.value = ''
    try {
        const { data } = await axios.get('/IncomeByYear')

        if (!Array.isArray(data)) {
            console.warn('Not array:', data)
            throw new Error('非配列レスポンス')
        }
        rows.value = data
            .filter(row => row && typeof row.year === 'number')
            .sort((a, b) => a.year - b.year)
    }catch (err) {
        console.error(err)
        errorMessage.value = '年次データの取得に失敗しました'
    } finally {
        loading.value = false
    }
}

function goBack () {
    router.replace({ path: '/', query: {year: props.year} })
}

onMounted(loadYearlySummary)

const yearLabels = computed(() => rows.value.map(row => String(row.year)))
const yearIncome = computed(() => rows.value.map(row => row.income))
const yearDeduction = computed(() => rows.value.map(row => row.deduction))
const yearNet = computed(() => rows.value.map(row => row.net))
</script>

<template>
  <div>
    <!-- Back -->
    <div class="mb-6">
      <button
        @click="goBack"
        class="text-sm text-gray-500 hover:text-gray-800 flex items-center gap-1"
      >
        &#8592; {{ props.year }}年へ戻る
      </button>
    </div>

    <h1 class="text-2xl font-bold text-gray-800 mb-6">年別所得</h1>

    <!-- Chart -->
    <div v-if="loading" class="text-gray-400 text-center py-10">Loading...</div>
    <div v-else-if="errorMessage" class="text-red-500 text-center">{{ errorMessage }}</div>
    <div v-else class="mb-8">
      <div class="h-[360px]">
        <YearLineChart
          :labels="yearLabels"
          :income="yearIncome"
          :deduction="yearDeduction"
          :net="yearNet"
          title="年別 収入 / 控除 / 手取り 推移"
          class="w-full max-w-2xl mx-auto"
        />
      </div>
    </div>

    <!-- Table -->
    <div v-if="!loading && !errorMessage" class="max-w-2xl mx-auto bg-white shadow rounded-lg overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr class="bg-gray-100 text-gray-600 text-left">
            <th class="px-5 py-3">年</th>
            <th class="px-5 py-3 text-right">収入</th>
            <th class="px-5 py-3 text-right">控除</th>
            <th class="px-5 py-3 text-right">手取り</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="row in rows"
            :key="row.year"
            class="border-t hover:bg-gray-50"
          >
            <td class="px-5 py-3 font-medium">{{ row.year }}年</td>
            <td class="px-5 py-3 text-right text-blue-600">{{ row.income.toLocaleString() }}</td>
            <td class="px-5 py-3 text-right text-red-500">{{ row.deduction.toLocaleString() }}</td>
            <td class="px-5 py-3 text-right text-green-600">{{ row.net.toLocaleString() }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
