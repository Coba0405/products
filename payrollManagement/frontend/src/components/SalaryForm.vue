<template>
  <div>
  <div class="max-w-2xl mx-auto">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6 anim-fade-up">
      <h2 class="text-xl font-extrabold text-slate-900 tracking-tight">
        {{ year }}年{{ month ? ' ' + month : '' }} の給与入力
      </h2>
      <button type="button" @click="$router.back()" class="text-sm text-slate-400 hover:text-slate-700 transition-colors">
        ✕ 閉じる
      </button>
    </div>

    <!-- リアルタイム手取りプレビュー（スクロール追従） -->
    <div class="sticky top-[68px] z-10 anim-fade-up" style="animation-delay: 50ms">
      <div class="bg-gradient-to-r from-ink-800 to-ink-900 text-white rounded-2xl px-5 py-4 mb-6 flex items-center justify-between shadow-hero">
        <div class="flex gap-6 text-sm">
          <div>
            <span class="text-[11px] text-slate-400 block mb-0.5">収入</span>
            <span class="text-blue-300 tabular-nums font-semibold">{{ animatedIncome.toLocaleString() }} 円</span>
          </div>
          <div>
            <span class="text-[11px] text-slate-400 block mb-0.5">控除</span>
            <span class="text-rose-300 tabular-nums font-semibold">{{ animatedDeduction.toLocaleString() }} 円</span>
          </div>
        </div>
        <div class="text-right">
          <span class="text-[11px] text-teal-300/90 tracking-widest uppercase block mb-0.5">手取り</span>
          <span :class="['text-2xl font-extrabold tabular-nums leading-none', previewNet < 0 ? 'text-rose-400' : 'text-teal-300']">{{ animatedNet.toLocaleString() }} 円</span>
        </div>
      </div>
    </div>

    <form @submit.prevent="submitForm" class="space-y-6">
      <!-- 年・月 -->
      <div class="grid grid-cols-2 gap-4 anim-fade-up" style="animation-delay: 100ms">
        <div class="flex flex-col gap-1.5">
          <label class="field-label">年</label>
          <input v-model.number="form.year" type="number" class="input-field" required />
        </div>
        <div class="flex flex-col gap-1.5">
          <label class="field-label">月</label>
          <select v-model="form.month" class="input-field" required>
            <option value="" disabled>選択してください</option>
            <option v-for="m in months" :key="m" :value="m">{{ m }}</option>
          </select>
        </div>
      </div>

      <!-- 会社名 -->
      <div class="flex flex-col gap-1.5 anim-fade-up" style="animation-delay: 140ms">
        <label class="field-label">会社名</label>
        <input v-model="form.company" type="text" class="input-field" required />
      </div>

      <!-- 支給 -->
      <div class="card anim-fade-up" style="animation-delay: 180ms">
        <div class="flex items-center gap-2 px-4 py-3 border-b border-slate-100">
          <span class="w-2 h-2 rounded-full bg-blue-500"></span>
          <h3 class="text-xs font-bold text-slate-700 tracking-widest">支給</h3>
        </div>
        <div class="grid grid-cols-2 gap-4 p-4">
          <div class="flex flex-col gap-1.5">
            <label class="field-label">基本給</label>
            <input v-model.number="form.base_salary" type="number" class="input-field" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="field-label">時間外勤務</label>
            <input v-model.number="form.overtime_pay" type="number" class="input-field" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="field-label">各種手当</label>
            <input v-model.number="form.allowances" type="number" class="input-field" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="field-label">非課税通勤手当（交通費）</label>
            <input v-model.number="form.transport" type="number" class="input-field" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="field-label">立替経費（支給）</label>
            <input v-model.number="form.expense_reimburse" type="number" class="input-field" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="field-label">遅早控除</label>
            <input v-model.number="form.lateness_deduction" type="number" class="input-field" placeholder="マイナスで入力" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="field-label">その他収入</label>
            <input v-model.number="form.income_other" type="number" class="input-field" />
          </div>
        </div>
      </div>

      <!-- 控除 -->
      <div class="card anim-fade-up" style="animation-delay: 220ms">
        <div class="flex items-center gap-2 px-4 py-3 border-b border-slate-100">
          <span class="w-2 h-2 rounded-full bg-rose-400"></span>
          <h3 class="text-xs font-bold text-slate-700 tracking-widest">控除</h3>
        </div>
        <div class="grid grid-cols-2 gap-4 p-4">
          <div class="flex flex-col gap-1.5">
            <label class="field-label">健康保険料</label>
            <input v-model.number="form.health_insurance" type="number" class="input-field" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="field-label">子ども子育て支援金</label>
            <input v-model.number="form.child_care_support" type="number" class="input-field" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="field-label">厚生年金</label>
            <input v-model.number="form.pension" type="number" class="input-field" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="field-label">雇用保険料</label>
            <input v-model.number="form.employment_insurance" type="number" class="input-field" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="field-label">介護保険料</label>
            <input v-model.number="form.nursing_insurance" type="number" class="input-field" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="field-label">所得税</label>
            <input v-model.number="form.income_tax" type="number" class="input-field" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="field-label">住民税</label>
            <input v-model.number="form.resident_tax" type="number" class="input-field" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="field-label">当月立替経費（控除）</label>
            <input v-model.number="form.reimburse_deduction" type="number" class="input-field" placeholder="天引きはマイナスで入力" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="field-label">ワーケーション費用</label>
            <input v-model.number="form.workation_fee" type="number" class="input-field" placeholder="天引きはマイナスで入力" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="field-label">その他控除</label>
            <input v-model.number="form.deduction_other" type="number" class="input-field" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="field-label">還付金</label>
            <input v-model.number="form.refund" type="number" class="input-field" />
          </div>
        </div>
      </div>

      <!-- 勤怠 -->
      <div class="card anim-fade-up" style="animation-delay: 260ms">
        <div class="flex items-center gap-2 px-4 py-3 border-b border-slate-100">
          <span class="w-2 h-2 rounded-full bg-slate-400"></span>
          <h3 class="text-xs font-bold text-slate-700 tracking-widest">勤怠</h3>
        </div>
        <div class="grid grid-cols-2 gap-4 p-4">
          <div class="flex flex-col gap-1.5">
            <label class="field-label">勤務日数</label>
            <input v-model.number="form.working_days" type="number" class="input-field" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="field-label">有給休暇</label>
            <input v-model.number="form.paid_leave" type="number" class="input-field" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="field-label">就労時間</label>
            <input v-model.number="form.working_hours" type="number" class="input-field" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="field-label">法定内残業</label>
            <input v-model="form.overtime_in" type="text" class="input-field" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="field-label">法定外残業</label>
            <input v-model="form.overtime_out" type="text" class="input-field" />
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="field-label">休日出勤</label>
            <input v-model="form.holiday_work" type="text" class="input-field" />
          </div>
        </div>
      </div>

      <!-- メモ -->
      <div class="flex flex-col gap-1.5 anim-fade-up" style="animation-delay: 300ms">
        <label class="field-label">メモ</label>
        <textarea v-model="form.memo" rows="3" class="input-field"></textarea>
      </div>

      <!-- ボタン -->
      <div class="flex justify-end gap-3 pt-2 anim-fade-up" style="animation-delay: 340ms">
        <button type="button" @click="$router.back()" class="btn-ghost">
          キャンセル
        </button>
        <button type="submit" :disabled="submitting" class="btn-primary !px-7">
          <span v-if="submitting" class="w-4 h-4 border-2 border-white/40 border-t-white rounded-full animate-spin"></span>
          {{ submitting ? '保存中...' : (id ? '更新' : '登録') }}
        </button>
      </div>
    </form>
  </div>

  <ToastNotification ref="toast" />
  </div>
</template>

<script setup>
import { reactive, ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import ToastNotification from './ToastNotification.vue'
import { useCountUp } from '../composables/useCountUp'

const route  = useRoute()
const router = useRouter()
const id = route.params.id
const toast = ref(null)
const submitting = ref(false)

const months = [
  '1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月',
  '夏季賞与','冬季賞与','特別賞与'
]

const initialYear  = Number(route.query.year)  || new Date().getFullYear()
const initialMonth =       route.query.month   || ''

const form = reactive({
  year: initialYear,
  month: initialMonth,
  company: '',
  base_salary: 0,
  overtime_pay: 0,
  allowances: 0,
  transport: 0,
  expense_reimburse: 0,
  income_other: 0,
  lateness_deduction: 0,
  health_insurance: 0,
  pension: 0,
  employment_insurance: 0,
  nursing_insurance: 0,
  child_care_support: 0,
  income_tax: 0,
  resident_tax: 0,
  reimburse_deduction: 0,
  workation_fee: 0,
  deduction_other: 0,
  refund: 0,
  working_days: 0,
  paid_leave: 0,
  working_hours: 0,
  overtime_in: '',
  overtime_out: '',
  holiday_work: '',
  late_early_time: '',
  memo: ''
})

/* リアルタイム手取りプレビュー */
const previewIncome = computed(() =>
  (form.base_salary || 0) + (form.overtime_pay || 0) + (form.allowances || 0) +
  (form.transport || 0) + (form.expense_reimburse || 0) + (form.income_other || 0) +
  (form.lateness_deduction || 0)
)
const previewDeduction = computed(() =>
  (form.health_insurance || 0) + (form.pension || 0) + (form.employment_insurance || 0) +
  (form.nursing_insurance || 0) + (form.child_care_support || 0) + (form.income_tax || 0) +
  (form.resident_tax || 0) + (form.reimburse_deduction || 0) + (form.workation_fee || 0) +
  (form.deduction_other || 0) - (form.refund || 0)
)
const previewNet = computed(() => previewIncome.value - previewDeduction.value)

/* 入力のたびに数字が滑らかに変化する */
const animatedIncome = useCountUp(previewIncome, 450)
const animatedDeduction = useCountUp(previewDeduction, 450)
const animatedNet = useCountUp(previewNet, 450)

const year  = computed(() => form.year)
const month = computed(() => form.month)

onMounted(async () => {
  if (id) {
    const { data } = await axios.get(`/api/salaries/${id}`)
    if (data && data.id) {
      Object.assign(form, data)
    } else {
      toast.value?.show('レコードが見つかりません', 'error')
    }
  }
})

async function submitForm () {
  submitting.value = true
  try {
    if (id) {
      await axios.put(`/api/salaries/${id}`, form)
      toast.value?.show('更新しました', 'success')
    } else {
      await axios.post('/api/salaries', form)
      toast.value?.show('登録しました', 'success')
    }
    setTimeout(() => router.back(), 800)
  } catch (e) {
    toast.value?.show('保存に失敗しました', 'error')
  } finally {
    submitting.value = false
  }
}
</script>
