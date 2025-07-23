<template>
  <div class="border p-6 rounded shadow-md bg-white max-w-lg mx-auto">
    <h3 class="text-xl font-hold mb-4 text-center">
      {{ props.year }}年 {{  props.month }}月の給与入力
    </h3>

    <!-- 入力フォーム本体 -->
    <form @submit.prevent="submitForm" class="space-y-3">
      <!-- 会社名 -->
      <div>
        <label class="block text-sm mb-1">会社名</label>
        <input v-model="form.company" type="text" class="input bg-gray-300" required />
      </div>

      <!-- ───── 収入 ───── -->
      <div><label class="block text-sm mb-1">基本給
          <input v-model.number="form.base_salary"    type="number" class="input bg-gray-300" />
      </label></div>

      <div><label class="block text-sm mb-1">時間外勤務
          <input v-model.number="form.overtime_pay"   type="number" class="input bg-gray-300" />
      </label></div>

      <div><label class="block text-sm mb-1">各種手当
          <input v-model.number="form.allowances"     type="number" class="input bg-gray-300" />
      </label></div>

      <div><label class="block text-sm mb-1">交通費
          <input v-model.number="form.transport"      type="number" class="input bg-gray-300" />
      </label></div>

      <div><label class="block text-sm mb-1">立替経費
          <input v-model.number="form.expense_reimburse" type="number" class="input bg-gray-300" />
      </label></div>

      <div><label class="block text-sm mb-1">その他収入
          <input v-model.number="form.income_other"   type="number" class="input bg-gray-300" />
      </label></div>

      <!-- ───── 控除 ───── -->
      <div><label class="block text-sm mb-1">健康保険料
          <input v-model.number="form.health_insurance" type="number" class="input bg-gray-300" />
      </label></div>

      <div><label class="block text-sm mb-1">厚生年金保険料
          <input v-model.number="form.pension"        type="number" class="input bg-gray-300" />
      </label></div>

      <div><label class="block text-sm mb-1">雇用保険料
          <input v-model.number="form.employment_insurance" type="number" class="input bg-gray-300" />
      </label></div>

      <div><label class="block text-sm mb-1">介護保険料
          <input v-model.number="form.nursing_insurance"  type="number" class="input bg-gray-300" />
      </label></div>

      <div><label class="block text-sm mb-1">社会保険料
          <input v-model.number="form.social_insurance"  type="number" class="input bg-gray-300" />
      </label></div>

      <div><label class="block text-sm mb-1">所得税
          <input v-model.number="form.income_tax"     type="number" class="input bg-gray-300" />
      </label></div>

      <div><label class="block text-sm mb-1">住民税
          <input v-model.number="form.resident_tax"   type="number" class="input bg-gray-300" />
      </label></div>

      <div><label class="block text-sm mb-1">その他控除
          <input v-model.number="form.deduction_other" type="number" class="input bg-gray-300" />
      </label></div>

      <div><label class="block text-sm mb-1">還付金
          <input v-model.number="form.refund"         type="number" class="input bg-gray-300" />
      </label></div>

      <!-- ───── 勤怠 ───── -->
      <div><label class="block text-sm mb-1">勤務日数
          <input v-model.number="form.working_days"   type="number" class="input bg-gray-300" />
      </label></div>

      <div><label class="block text-sm mb-1">有給休暇
          <input v-model.number="form.paid_leave"     type="number" class="input bg-gray-300" />
      </label></div>

      <div><label class="block text-sm mb-1">就労時間
          <input v-model.number="form.working_hours"  type="number" class="input bg-gray-300" />
      </label></div>

      <div><label class="block text-sm mb-1">法定内残業
          <input v-model="form.overtime_in"           type="text"   class="input bg-gray-300" />
      </label></div>

      <div><label class="block text-sm mb-1">法定外残業
          <input v-model="form.overtime_out"          type="text"   class="input bg-gray-300" />
      </label></div>

      <div><label class="block text-sm mb-1">休日出勤
          <input v-model="form.holiday_work"          type="text"   class="input bg-gray-300" />
      </label></div>

      <!-- ───── メモ ───── -->
      <div>
        <label class="block text-sm mb-1">メモ</label>
        <textarea v-model="form.memo" rows="3" class="input bg-gray-300"></textarea>
      </div>

      <div class="flex justify-end gap-3 pt-4">
        <button type="button" @click="$emit('close')" class="text-sm text-gray-500">閉じる</button>
        <button type="submit" class="bg-blue-600 text-white px-4 py-1 rounded">登録</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { defineProps, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

// propsで年と年を受け取る
// const props =defineProps({
//   id: String,
//   initialYear: { type: Number, required: true },
//   initialMonth: {type: String, required: true}
// })

// 登録後or閉じる用のemit
// defineEmits(['close'])

// formの初期値をpropsでセットする
// const form = reactive({
//   year: props.initialYear,
//   month: props.initialMonth,
//   company: '',
//   base_salary: 0,
//   overtime_pay: 0,
//   holiday_work: 0
// })

// onMounted(async () => {
//   if (props.id) {
//     const { data } =await axios.get(`/apo/salaries/${props.id}`)
//     console.log('えでぃっと data', data)
//     Object.assign(form, data)
//   }
// })

// async function submitForm (){
//   try {
//     if (props.id) {
//       await axios.put(`/api/salaries/${props.id}`, form)
//       alert('更新しました')
//     } else {
//       await axios.post('/api/salaries', form)
//       alert('登録しました')
//     }
//     emit('close')
//   }
//   catch (err) {
//     console.error(err)
//     alert('通信に失敗しました')
//   }
// }


const id = route.params.id || null
const initialYear = Number(route.query.year) || new Date().getFullYear()
const initialMonth = route.query.month || ''

const form = reactive({
  year: initialYear,
  month: initialMonth,
  company: '',
  base_salary: 0,
  overtime_pay: 0,
  holiday_work: 0
})

onMounted(async () => {
  if(id) {
    const {data} 
  }
})

</script>
