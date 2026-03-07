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
        <div class="bg-blue-700 text-white text-center font-semibold py-1.5 text-sm">
            {{ title }}
        </div>

        <table class="w-full flex-1">
            <tbody>
                <tr
                  v-for="[label,val] in rows"
                  :key="label"
                  :class="[
                    'border-t',
                    label === '合計' || label === '差引支給額'
                      ? 'bg-gray-50 font-semibold'
                      : ''
                  ]"
                >
                    <td class="px-3 py-1.5 text-sm">{{ label }}</td>
                    <td class="px-3 py-1.5 text-right text-sm">{{ val }}</td>
                </tr>
                <tr v-if="rows.length === 0">
                    <td class="h-24 bg-gray-50" colspan="2"></td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
