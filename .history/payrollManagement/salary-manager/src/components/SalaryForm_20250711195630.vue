<template>
  <div class="border p-6 rounded shadow-md bg-white max-w-lg mx-auto">
    <h3 class="text-xl font-hold mb-4 text-center">
      {{ form.year }}年 {{  form.month }}月の給与入力
    </h3>

    <!-- 入力フォーム本体 -->
    <form @submit.prevent="submitForm" class="space-y-3">
      <div>
        <label class="block text-sm mb-1">会社名</label>
        <input v-model.number="form.company" type="text" class="input " required />
      </div>

      <div>
        <label class="block text-sm mb-1">基本給</label>
        <input v-model.number="form.base_salary" type="number" class="input" />
      </div>

      <div>
        <label class="block text-sm mb-1">時間外勤務</label>
        <input v-model.number="form.overtime_pay" type="number" class="input" />
      </div>

      <div>
        <label class="block text-sm mb-1">休日出勤</label>
        <input v-model.number="form.holiday_work" type="number" class="input" />
      </div>

      <!-- 他の項目も後ほどここに追加 -->

      <div class="flex justify-end gap-3 pt-4">
        <button type="button" @click="$emit('close')" class="text-sm text-gray-500">閉じる</button>
        <button type="submit" class="bg-blue-600 text-white px-4 py-1 rounded">登録</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { defineProps, reactive, onMounted } from 'vue'
import axios from 'axios'

// propsで年と年を受け取る
const props =defineProps({
  initialYear: { type: Number, required: true },
  initialMonth: {type: String, required: true},
  id: String
})

// 登録後or閉じる用のemit
defineEmits(['close'])

// formの初期値をpropsでセットする
const form = reactive({
  year: props.initialYear,
  month: props.initialMonth,
  company: '',
  base_salary: 0,
  overtime_pay: 0,
  holiday_work: 0
})

onMounted(async () => {
  if (props.id) {
    const { data } =await axios.get(`/apo/salaries/${props.id}`)
    Object.assign(form, data)
  }
})

async function submitForm (){
  try {
    if (props.id) {
      await axios.put(`/api/salaries/${props.id}`, form)
      alert('更新しました')
    } else {
      await axios.post('/api/salaries', form)
      alert('登録しました')
    }
    emit('close')
  }
  catch (err) {
    console.error(err)
    alert('通信に失敗しました')
  }
}
</script>
