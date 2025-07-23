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
    { path: '/salary/:year(\\d{4})/:month', component: SalaryView, props: true },
    // 年別所得のグラフ表示
    { path: '/IncomeByYear', component: IncomeByYear},
]

export default createRouter({
    history: createWebHistory(),
    routes
})
