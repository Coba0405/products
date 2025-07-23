import { createRouter, createWebHistory } from 'vue-router'
import YearlySummary from '../components/YearlySummary.vue'
import SalaryView from '../components/SalaryView.vue'
import SalaryForm from '../components/SalaryForm.vue'

const routes = [
    { path: '/', component: YearlySummary },
    // idなしの新規入力
    { path: '/salary/new', component: SalaryForm },
    // idありの場合編集
    { path: '/salary/:id(\\d+)/edit',
        component: SalaryForm,
        props: route => ({ id: Number(route.params.id) })
    },
    // 明細表示
    { path: '/salary/:year(\\d{4})/:month', component: SalaryView, props: true },
]

export default createRouter({
    history: createWebHistory(),
    routes
})
