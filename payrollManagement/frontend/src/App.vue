<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header Nav -->
    <header class="bg-white border-b shadow-sm sticky top-0 z-10">
      <div class="max-w-4xl mx-auto px-6 py-3 flex items-center justify-between">
        <router-link to="/" class="text-lg font-bold text-gray-800 hover:text-blue-600">
          給与明細管理
        </router-link>
        <nav class="flex items-center gap-3 text-sm">
          <router-link
            to="/"
            class="text-gray-600 hover:text-blue-600 font-medium px-2 py-1 rounded hover:bg-gray-100"
          >
            ホーム
          </router-link>
          <router-link
            :to="{ name: 'income-by-year' }"
            class="text-gray-600 hover:text-blue-600 font-medium px-2 py-1 rounded hover:bg-gray-100"
          >
            年別所得
          </router-link>
          <router-link
            :to="{ name: 'withholding-tax', params: { year: new Date().getFullYear() } }"
            class="text-gray-600 hover:text-blue-600 font-medium px-2 py-1 rounded hover:bg-gray-100"
          >
            源泉徴収票
          </router-link>
          <router-link
            to="/salary/new"
            class="bg-blue-600 text-white px-4 py-1.5 rounded-lg hover:bg-blue-700 font-medium"
          >
            + 新規入力
          </router-link>
        </nav>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-4xl mx-auto px-6 py-8">
      <router-view />
    </main>
  </div>
</template>

<script setup>
</script>
