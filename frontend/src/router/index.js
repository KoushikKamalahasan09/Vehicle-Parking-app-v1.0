import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '@/views/auth/login.vue'
import Register from '@/views/auth/register.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [


    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path:'/login',
      name: 'login',
      component: Login, 
    },
    {
      path : '/register',
      name: 'register',
      component: Register,
    },
    {
      path:'/admin/dashboard',
      name: 'admin-dashboard',
      component: () => import('../views/admin/dashboard.vue'),
    },
    {
      path:'/admin/users',
      name: 'admin-users',
      component: () => import('../views/admin/list_users.vue'),
    },
    {
      path:'/admin/parkinglots',
      name: 'admin-lots',
      component: () => import('../views/admin/Parkinglots.vue'),
    },
    {
      path:'/admin/parkinglots/:lot_id',
      name: 'admin-lot-details',
      component: () => import('../views/admin/Parkingspots.vue'),
    },
    {
      path:'/admin/profile',
      name: 'admin_profile',
      component: ()=> import ('../views/admin/profile.vue'), // Admin Profile view
    },
    {
      path:'/admin/summary',
      name: 'admin_summary',
      component: () => import('../views/admin/summary.vue'), // Lazy-loaded Admin Summary
    },
    {
      path:'/admin/user/:user_id/summary',
      name: 'admin_user_summary',
      component: () => import('../views/admin/user_summary.vue'), // Lazy-loaded Admin User Summary
    },
        {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/User/dashboard.vue'),
    },
    {
      path:'/profile',
      name: 'profile',
      component: () => import('../views/User/profile.vue'),
    },
    {
      path:'/reservations',
      name: 'user_reservations',
      component: () => import('../views/User/reservations.vue'), // Lazy-loaded User Reservations
    },
    {
      path:'/summary',
      name: 'user_summary',
      component: () => import('../views/User/summary.vue'), // Lazy-loaded User Summary
    },

  ],
})

export default router
