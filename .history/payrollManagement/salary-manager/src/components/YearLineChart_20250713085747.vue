<template>
    <!--  親要素の高さで可変にしたいなら h-64 とかを付ける  -->
    <Line :data="data" :options="optopns" class="w-full" h-64 />
    import {}
</template>

<script setup>
import { Line } from 'vue-chartjs'
</script>
