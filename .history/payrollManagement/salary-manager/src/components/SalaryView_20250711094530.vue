<template>
    <div v-if="detail" class="p-6">
        <h2 class="text-xl font-bold mb-4">{{ props.year }}年 {{ props.month }} 月明細</h2>
        <p>会社名: {{ detail.company }}</p>
        <p>基本給: {{ detail.base_salary.toLocaleString() }} 円</p>
        <!-- いか必要な項目を入れる -->
    </div>

    <p v-else-if="isError" class="text-red-500">データの取得に失敗しました</p>
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