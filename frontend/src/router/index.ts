import { createRouter, createWebHistory } from 'vue-router'
import OperatorDetailsView from '../views/OperatorDetailsView.vue'
import OperatorListView from '../views/OperatorListView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: OperatorListView,
    },
    {
      path: '/operadora/:id',
      name: 'operator-details',
      component: OperatorDetailsView,
    },
  ],
})

export default router
