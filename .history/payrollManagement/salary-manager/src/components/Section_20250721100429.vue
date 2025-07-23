<!-- 親コンポーネント SalaryView.vue -->
<script setup>
defineProps({
    title: String,
    rows: Array,
    outerClass: { type: String, default: '' }
})
</script>

<template>
    <div :class="['border rounded flex flex-col h-full', outerClass]">
        <div class="bg-blue-700 text-white text-center font-semibold py-1">
            {{ title }}
        </div>

        <table class="w-full flex-1">
            <tbody class="">
                <!-- rowsの配列[0]に'label',[1]に'val'と名前をつけている -->
                <tr v-for="[label,val] in rows" :key="label" class="border-line mt-auto">
                    <td class="border-t px-2 text-sm">{{ label }}</td>
                    <td class="border-t px-2 text-right text-sm">{{ val }}</td>
                </tr>
                <tr v-if="rows.length === 0">
                    <td class="h-24 bg-gray-50" colspan="2"></td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
