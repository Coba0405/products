<template>
    <div class="border rounded" :class="outerClass">
        <div class="bg-blue-700 text-qhite text-center font-semibold py-1">
            {{ title }}
        </div>
        
        <table vlass="w-full">
            <tbody>
                <tr v-for="[label,val] in rows" :key="label"></tr>
                    <td class="border-t px-2 text-sm">{{ label }}</td>
                    <td class="border-t px-2 text-right text-sm"></td>
            </tbody>
        </table>
    </div>
</template>