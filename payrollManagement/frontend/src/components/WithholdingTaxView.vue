<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const props = defineProps({
  year: { type: Number, required: true }
})

const router = useRouter()
const data = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const { data: res } = await axios.get(`/api/withholding_tax/${props.year}`)
    data.value = res
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})

const fmt = v => typeof v === 'number' ? v.toLocaleString() + ' 円' : (v || '—')

async function onDelete() {
  if (!confirm('本当に削除しますか？')) return
  try {
    await axios.delete(`/api/withholding_tax/${data.value.id}`)
    alert('削除しました')
    router.push({ path: '/', query: { year: props.year } })
  } catch (e) {
    alert('削除に失敗しました')
  }
}
</script>

<template>
  <div>
    <!-- Top bar -->
    <div class="flex items-center justify-between mb-6">
      <button
        @click="$router.push({ path: '/', query: { year: props.year } })"
        class="text-sm text-gray-500 hover:text-gray-800 flex items-center gap-1"
      >
        &#8592; {{ props.year }}年へ戻る
      </button>
      <div v-if="data" class="flex gap-2">
        <router-link
          :to="{ name: 'withholding-tax-edit', params: { id: data.id }, query: { year: data.year } }"
          class="bg-blue-600 text-white text-sm px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          編集
        </router-link>
        <button
          @click="onDelete"
          class="bg-red-500 text-white text-sm px-4 py-2 rounded-lg hover:bg-red-600"
        >
          削除
        </button>
      </div>
    </div>

    <h2 class="text-2xl font-bold text-gray-800 mb-1">{{ props.year }}年 源泉徴収票</h2>

    <div v-if="loading" class="text-gray-400 py-10 text-center">読み込み中...</div>

    <!-- 未登録 -->
    <div v-else-if="!data" class="text-center py-16">
      <p class="text-gray-500 mb-6">{{ props.year }}年の源泉徴収票はまだ登録されていません</p>
      <router-link
        :to="{ name: 'withholding-tax-new', query: { year: props.year } }"
        class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 font-medium"
      >
        + 登録する
      </router-link>
    </div>

    <!-- 表示 -->
    <div v-else>
      <p class="text-sm text-gray-500 mb-6">{{ data.company }}</p>

      <div class="max-w-lg mx-auto space-y-4">
        <!-- 支払・所得 -->
        <div class="bg-white shadow rounded-lg overflow-hidden">
          <div class="bg-blue-700 text-white text-center font-semibold py-2 text-sm">支払・所得</div>
          <table class="w-full text-sm">
            <tbody>
              <tr class="border-t">
                <td class="px-4 py-2 text-gray-600">支払金額</td>
                <td class="px-4 py-2 text-right font-medium">{{ fmt(data.payment_amount) }}</td>
              </tr>
              <tr class="border-t">
                <td class="px-4 py-2 text-gray-600">給与所得控除後の金額</td>
                <td class="px-4 py-2 text-right font-medium">{{ fmt(data.after_deduction) }}</td>
              </tr>
              <tr class="border-t">
                <td class="px-4 py-2 text-gray-600">所得控除の額の合計額</td>
                <td class="px-4 py-2 text-right font-medium">{{ fmt(data.total_income_deduction) }}</td>
              </tr>
              <tr class="border-t bg-gray-50 font-semibold">
                <td class="px-4 py-2 text-gray-700">源泉徴収税額</td>
                <td class="px-4 py-2 text-right">{{ fmt(data.withholding_tax_amount) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 各種控除 -->
        <div class="bg-white shadow rounded-lg overflow-hidden">
          <div class="bg-blue-700 text-white text-center font-semibold py-2 text-sm">各種控除</div>
          <table class="w-full text-sm">
            <tbody>
              <tr class="border-t">
                <td class="px-4 py-2 text-gray-600">社会保険料等の金額</td>
                <td class="px-4 py-2 text-right">{{ fmt(data.social_insurance_amount) }}</td>
              </tr>
              <tr class="border-t">
                <td class="px-4 py-2 text-gray-600">生命保険料の控除額</td>
                <td class="px-4 py-2 text-right">{{ fmt(data.life_insurance_deduction) }}</td>
              </tr>
              <tr class="border-t">
                <td class="px-4 py-2 text-gray-600">地震保険料の控除額</td>
                <td class="px-4 py-2 text-right">{{ fmt(data.earthquake_insurance_deduction) }}</td>
              </tr>
              <tr class="border-t">
                <td class="px-4 py-2 text-gray-600">住宅借入金等特別控除の額</td>
                <td class="px-4 py-2 text-right">{{ fmt(data.housing_loan_deduction) }}</td>
              </tr>
              <tr class="border-t">
                <td class="px-4 py-2 text-gray-600">配偶者特別控除の額</td>
                <td class="px-4 py-2 text-right">{{ fmt(data.spouse_deduction) }}</td>
              </tr>
              <tr class="border-t">
                <td class="px-4 py-2 text-gray-600">扶養親族の数</td>
                <td class="px-4 py-2 text-right">{{ data.dependent_count }} 人</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- メモ -->
        <div v-if="data.memo" class="bg-white shadow rounded-lg p-4 text-sm text-gray-600">
          {{ data.memo }}
        </div>
      </div>
    </div>
  </div>
</template>
