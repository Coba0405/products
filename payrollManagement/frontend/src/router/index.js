import { createRouter, createWebHistory } from 'vue-router'
import YearlySummary from '../components/YearlySummary.vue'
import SalaryView from '../components/SalaryView.vue'
import SalaryForm from '../components/SalaryForm.vue'
import IncomeByYear from '../components/IncomeByYear.vue'
import WithholdingTaxView from '../components/WithholdingTaxView.vue'
import WithholdingTaxForm from '../components/WithholdingTaxForm.vue'

const routes = [
    { path: '/', component: YearlySummary },
    { path: '/salary/new', component: SalaryForm },
    { path: '/salary/:id(\\d+)/edit',
      name : 'salary-edit',
      component: SalaryForm,
      props: route => ({ id: Number(route.params.id) })
    },
    { path: '/salary/:year(\\d{4})/:month',
      component: SalaryView,
      props: route => ({
        year: Number(route.params.year),
        month: route.params.month
      })
    },
    { path: '/income/by_year',
      name: 'income-by-year',
      component: IncomeByYear,
      props: route => ({
        year: Number(route.query.year) || new Date().getFullYear()
      })
    },
    { path: '/withholding-tax/new',
      name: 'withholding-tax-new',
      component: WithholdingTaxForm
    },
    { path: '/withholding-tax/:id(\\d+)/edit',
      name: 'withholding-tax-edit',
      component: WithholdingTaxForm
    },
    { path: '/withholding-tax/:year(\\d{4})',
      name: 'withholding-tax',
      component: WithholdingTaxView,
      props: route => ({ year: Number(route.params.year) })
    },
]

export default createRouter({
    history: createWebHistory(),
    routes
})
