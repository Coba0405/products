import { createRouter, createWebHistory } from 'vue-router'
import YearlySummary from '../components/YearlySummary.vue'
import SalaryView from '../components/SalaryView.vue'
import SalaryForm from '../components/SalaryForm.vue'

const routes = [
    { path: '/', component: YearlySummary },
    { path: '/salar'}
    { path: '/salary/:id(\\d+)/edit', component: SalaryView, props: true },
    { path: '/salary/:year(\\d{4})/:month', component: SalaryView, props: true }
]

export default createRouter({
    history: createWebHistory(),
    routes
})
