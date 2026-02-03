import { createRouter, createWebHistory } from 'vue-router'
import CompanyDetailsView from '../views/CompanyDetailsView.vue'
import CompanyListView from '../views/CompanyListView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: CompanyListView,
    },
    {
      path: '/operadora/:cnpj',
      name: 'Company-details',
      component: CompanyDetailsView,
    },
  ],
})

export default router
