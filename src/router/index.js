import { createRouter, createWebHistory } from 'vue-router'
import Inicio_Principal from '../views/Inicio_Principal.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Inicio_Principal,
    },
  ],
})

export default router
