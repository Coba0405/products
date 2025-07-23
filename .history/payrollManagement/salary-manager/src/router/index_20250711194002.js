import { createRouter, createWebHistory } from 'vue-router'
import YearlySummary from '../components/YearlySummary.vue'
import SalaryView from '../components/SalaryView.vue'

const routes = [
    { path: '/', component: YearlySummary },
    { path: '/salary/:id(\\d+)/edit', component: SalaryView, props: true },
    { path: '/salary/:yea(r/:month', component: SalaryView, props: true }
]

export default createRouter({
    history: createWebHistory(),
    routes
})
