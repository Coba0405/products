<template>
    <div class="border rounded" :class="outerClass">
        <div class="bg-blue-700 text-qhite text-center font-semibold py-1">
            {{ title }}
        </div>
        
        <table vlass="w-full">
            <tbody>
                <tr v-for="[label,val] in rows" :key="label">   
                    <td class="border-t px-2 text-sm">{{ label }}</td>
                    <td class="border-t px-2 text-right text-sm">{{ val }}</td>
                </tr>
                <tr v-if="rows.length === 0">
                    <td class="h-24 bg-gray-50" colspan~></td>
                </tr>
            </tbody>
        </table>
    </div>
</template>