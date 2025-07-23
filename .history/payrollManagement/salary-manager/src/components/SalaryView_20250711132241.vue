<template>
  <div v-if="detail" class="p-6">
    <h2 class="text-2xl font-bold mb-6">
      {{ props.year }}年 {{ props.month }} の給与明細
    </h2>

    <!-- ▼ 横3列テーブル（勤怠 | 収入 | 控除）-->
    <table class="w-full border-collapse">
      <thead>
        <tr class="bg-gray-200 text-center">
          <th class="border p-2 w-1/3">勤怠</th>
          <th class="border p-2 w-1/3">収入</th>
          <th class="border p-2 w-1/3">控除</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="i in maxRows" :key="i">
          <!-- 勤怠 -->
          <td class="border p-2">
            <template v-if="workRows[i-1]">
              {{ workRows[i-1][0] }}:&nbsp;{{ workRows[i-1][1] }}
            </template>
          </td>

          <!-- 収入 -->
          <td class="border p-2">
            <template v-if="incomeRows[i-1]">
              {{ incomeRows[i-1][0] }}:&nbsp;{{ fmt(incomeRows[i-1][1]) }}
            </template>
          </td>

          <!-- 控除 -->
          <td class="border p-2">
            <template v-if="deductRows[i-1]">
              {{ deductRows[i-1][0] }}:&nbsp;{{ fmt(deductRows[i-1][1]) }}
            </template>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- メモ -->
    <h3 class="font-semibold text-lg mt-6">メモ</h3>
    <p class="border p-3 rounded bg-gray-50 whitespace-pre-wrap">
      {{ detail.memo || '—' }}
    </p>
  </div>

  <p v-else-if="isError" class="text-red-600 p-4">データ取得に失敗しました</p>
  <p v-else class="p-4 text-center">読み込み中...</p>
</template>

<script setup>
import { defineProps, ref, onMounted, computed } from 'vue'
import axios from 'axios'

/* props (ルーターから渡ってくる) */
const props = defineProps({ year: String, month: String })

/* state */
const detail  = ref(null)
const isError = ref(false)

/* API 呼び出し（年 / 月の階層 URL 版）*/
onMounted(async () => {
  try {
    const { data } = await axios.get(
      `/api/salaries/${props.year}/${props.month}`
    )
    detail.value = data[0] ?? null          // 配列 → オブジェクト
  } catch (e) {
    isError.value = true
    console.error('明細取得失敗', e)
  }
})

/* ---- 表示用データ配列 ---- */
const incomeRows = computed(() => detail.value ? [
  ['基本給',        detail.value.base_salary      ],
  ['時間外勤務',    detail.value.overtime_pay     ],
  ['各種手当',      detail.value.allowances       ],
  ['交通費',        detail.value.transport        ],
  ['立替経費',      detail.value.expense_reimburse],
  ['その他収入',    detail.value.income_other     ],
] : [])

const deductRows = computed(() => detail.value ? [
  ['健康保険料',    detail.value.health_insurance ],
  ['厚生年金保険料',detail.value.pension          ],
  ['雇用保険料',    detail.value.employment_insurance],
  ['介護保険料',    detail.value.nursing_insurance],
  ['社会保険料',    detail.value.social_insurance ],
  ['所得税',        detail.value.income_tax       ],
  ['住民税',        detail.value.resident_tax     ],
  ['その他控除',    detail.value.deduction_other  ],
  ['還付金',       -detail.value.refund          ],
] : [])

const workRows = computed(() => detail.value ? [
  ['勤務日数',      detail.value.working_days ],
  ['有給休暇',      detail.value.paid_leave   ],
  ['就労時間',      detail.value.working_hours],
  ['法定内残業',    detail.value.overtime_in  ],
  ['法定外残業',    detail.value.overtime_out ],
  ['休日出勤',      detail.value.holiday_work ],
] : [])

/* 最大行数 */
const maxRows = computed(() =>
  Math.max(incomeRows.value.length,
           deductRows.value.length,
           workRows.value.length))

/* 数値→カンマ＋円、文字列はそのまま */
const fmt = v => typeof v === 'number' ? v.toLocaleString() + ' 円' : v
</script>