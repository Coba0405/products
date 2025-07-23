import { createRouter, createWebHistory } from 'vue-router'
import YearlySummary from '../components/YearlySummary.vue'
import SalaryView from '../components/SalaryView.vue'
import SalaryForm from '../components/SalaryForm.vue'

const routes = [
    { path: '/', component: YearlySummary },
    { path: '/salary/:id(\\d+)/edit', component: SalaryForm, props: true },
    { path}
    { path: '/salary/:year(\\d{4})/:month', component: SalaryView, props: true }
]

export default createRouter({
    history: createWebHistory(),
    routes
})
