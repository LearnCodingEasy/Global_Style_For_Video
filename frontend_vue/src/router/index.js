import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/Authentication/LoginView.vue'
import ProfileView from '../views/Account/ProfileView.vue'
import AuthCallback from '../views/Authentication/AuthCallback.vue'
import AuthCallback2 from '../views/Authentication/AuthCallback.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    // Authentication [ Login ]
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    // Account [ Profile ]
    {
      path: '/profile/:id',
      name: 'profile',
      component: ProfileView,
      meta: {
        requireLogin: true,
      },
    },
    {
      path: '/auth-callback',
      name: 'AuthCallback',
      component: AuthCallback,
    },
    {
      path: '/auth-callback',
      name: 'AuthCallback',
      component: AuthCallback2,
    },

    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
  ],
})

export default router
