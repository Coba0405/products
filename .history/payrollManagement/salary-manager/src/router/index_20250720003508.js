import { createRouter, createWebHistory } from 'vue-router'
import YearlySummary from '../components/YearlySummary.vue'
import SalaryView from '../components/SalaryView.vue'
import SalaryForm from '../components/SalaryForm.vue'
import IncomeByYear from '../components/IncomeByYear.vue'

const routes = [
    { path: '/', component: YearlySummary },
    // idなしの新規入力
    { path: '/salary/new', component: SalaryForm },
    // idありの場合編集
    { path: '/salary/:id(\\d+)/edit',
      name : 'salary-edit',
      component: SalaryForm,
      props: route => ({ id: Number(route.params.id) })
    },
    // 明細表示
    { path: '/salary/:year(\\d{4})/:month',
      component: SalaryView,
      props: route => ({
        year: Number(route.params.year),
        month: route.params.month
      })
    },
    // 年別所得のグラフ表示
    { path: '/IncomeByYear',
      name: 'Income-by-year',
      component: IncomeByYear,
      // クエリ ?year=YYYY がなければ今年
      props: route => ({
        year: Number(route.query.year) || new D
      })
    },
]

export default createRouter({
    history: createWebHistory(),
    routes
})
