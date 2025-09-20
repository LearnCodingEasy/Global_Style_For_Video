import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/Authentication/LoginView.vue'
import ProfileView from '../views/Account/ProfileView.vue'
import AuthCallback from '../views/Authentication/AuthCallback.vue'
import Vendors from '../views/Marketplace/VendorsView.vue'
import DetailVendor from '../views/Marketplace/VendorView.vue'
import EditVendor from '../views/Marketplace/EditVendorView.vue'
import Products from '../views/Marketplace/ProductsView.vue'
import Categories from '../views/Marketplace/Categories/CategoriesView.vue'
import AddCategoryView from '../views/Marketplace/Categories/AddCategoryView.vue'

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
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    // Vendors
    {
      path: '/Vendors',
      name: 'Vendors',
      component: Vendors,
    },
    {
      // path: '/Vendors/:id',
      // path: '/Vendors/DetailVendor/:id',
      path: '/:id',
      name: 'DetailVendor',
      component: DetailVendor,
    },
    {
      // path: '/Vendors/:id',
      path: '/:id/edit',
      name: 'EditVendor',
      component: EditVendor,
    },
    // Products
    {
      path: '/products',
      name: 'products',
      component: Products,
    },
    // Categories
    {
      path: '/Categories',
      name: 'Categories',
      component: Categories,
    },
    {
      path: '/AddCategoryView',
      name: 'AddCategoryView',
      component: AddCategoryView,
    },
    {
      // path: '/Categories/:id',
      // path: '/Categories/:id',
      // name: 'Category',
      // component: Category,
    },
  ],
})

export default router
