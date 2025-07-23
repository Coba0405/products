<template>
    <div v-if="detail" class="p-6">
        <h2 class="text-xl font-bold mb-4">{{ props.year }}年 {{ props.month }} 月明細</h2>
        <p>会社名: {{ detail.company }}</p>
        <h3>収入</h3>
        <p>基本給: {{ detail.base_salary.toLocaleString() }} 円</p>
        <p>時間外勤務: {{ detail.overtime_pay.toLocaleString() }}円</p>
        <p>各種手当: {{ detail.allowances.toLocaleString() }} 円</p>
        <p>交通費: {{ detail.transport.toLocaleString() }} 円</p>
        <p>立替経費: {{ detail.expense_reimburse.toLocaleString() }} 円</p>
        <p>その他収入: {{ detail.income_other.toLocaleString() }} 円</p>
        <h3>控除</h3>
        <p>健康保険料: {{ detail.health_insurance.toLocaleString() }} 円</p>
        <p>厚生年金保険料: {{ detail.pension.toLocaleString() }} 円</p>
        <p>雇用保険料: {{ detail.employment_insurance.toLocaleString() }} 円</p>
        <p>介護保険料: {{ detail.nursing_insurance.toLocaleString() }} 円</p>
        <p>社会保険料: {{ detail.social_insurance.toLocaleString() }} 円</p>
        <p>所得税: {{ detail.income_tax.toLocaleString() }} 円</p>
        <p>住民税: {{ detail.resident_tax.toLocaleString() }} 円</p>
        <p>その他控除: {{ detail.deduction_other.toLocaleString() }} 円</p>
        <p>還付金: {{ detail.refund.toLocaleString() }} 円</p>
        <h3>勤怠</h3>
        
    </div>

    <p v-else-if="isError" class="text-red-500">データの取得に失敗しました</p>
    <p v-else>読み込み中...</p>
</template>

<script setup>
import { defineProps, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const props = defineProps({
    year: String,
    month: String
})

const detail = ref(null)
const isError = ref(false)

onMounted(async () => {
    try {
        const res = await axios.get(`/api/salaries/${props.year}/${props.month}`)
        
        // res.dataは配列なので0要素目を取り出す
        detail.value = res.data[0] ?? null
    }
    catch (e) {
        isError.value = true
        console.error('明細取得失敗', e)
    }
})
</script>