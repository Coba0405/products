<template>
    <div v-if="detail" class="p-6">
        <h2 class="text-xl font-bold mb-4">{{ year }}年 {{ month }} 月明細</h2>
        <p>会社名: {{ detail.company }}</p>
        <p>基本給: {{ detail.base_salary.toLocaleString() }} 円</p>
        <!-- いか必要な項目を入れる -->
    </div>
</template>

<script setup>
    
</script>