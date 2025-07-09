<template>
    <form @submit.prevent="submitForm">
        <h2 class="text-xl font-bold mb-4">給与明細　登録フォーム</h2>

        <div class="mb-2">
            <label>年: <input v-model="form.year" type="number" min="2000" max="2099" required /></label>
        </div>

        <div class="mb-2">
            
        </div>
</template>