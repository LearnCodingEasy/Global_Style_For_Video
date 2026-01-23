import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'

// Explain
import ExplainsView from '../views/Explain/ExplainView.vue'
import ExplainDetails from '../views/Explain/ExplainDetails.vue'
import ExplainCreate from '../views/Explain/ExplainCreate.vue'
import ExplainEdit from '../views/Explain/ExplainEdit.vue'

import LoginView from '../views/Authentication/LoginView.vue'
import ProfileView from '../views/Account/ProfileView.vue'
import AuthCallback from '../views/Authentication/AuthCallback.vue'
import Vendors from '../views/Marketplace/VendorsView.vue'
import DetailVendor from '../views/Marketplace/VendorView.vue'
import EditVendor from '../views/Marketplace/EditVendorView.vue'

// Products
import Products from '../views/Marketplace/ProductsView.vue'
import Categories from '../views/Marketplace/Categories/CategoriesView.vue'
import AddCategory from '../views/Marketplace/Categories/AddCategoryView.vue'
// Automation
import Automation from '../views/Automation/AutomationView.vue'
import Dashboard from '../views/Automation/DashboardView.vue'
import ProgramList from '../views/Automation/ProgramList.vue'
import ProgramCreate from '../views/Automation/ProgramCreate.vue'
import ProgramEdit from '../views/Automation/ProgramEdit.vue'
import TaskCreate from '../views/Automation/TaskCreate.vue'
import TaskEditor from '../views/Automation/TaskEditor.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    // Explain
    {
      path: '/explains',
      name: 'explains',
      component: ExplainsView,
    },
    {
      path: '/explains/:id',
      name: 'explain-details',
      component: ExplainDetails,
      props: true,
    },
    {
      path: '/explains/explain_create',
      name: 'explain_create',
      component: ExplainCreate,
    },
    {
      path: '/explains/:id',
      name: 'explain_edit',
      component: ExplainEdit,
    },
    // Automation
    {
      path: '/automation',
      name: 'automation',
      component: Automation,
    },
    {
      path: '/automation_Dashboard',
      name: 'automation_Dashboard',
      component: Dashboard,
    },
    {
      path: '/automation_ProgramList',
      name: 'automation_ProgramList',
      component: ProgramList,
    },
    {
      path: '/automation_programs_create',
      name: 'automation_programs_create',
      component: ProgramCreate,
    },
    {
      path: '/automation/:id',
      name: 'automation_programs_edit',
      component: ProgramEdit,
    },
    {
      path: '/automation_TaskCreate',
      name: 'automation_TaskCreate',
      component: TaskCreate,
    },
    {
      path: '/automation_TaskEditor',
      name: 'automation_TaskEditor',
      component: TaskEditor,
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
      path: '/Vendors/:id',
      name: 'DetailVendor',
      component: DetailVendor,
    },
    {
      path: '/Vendors/:id/edit',
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
      path: '/AddCategory',
      name: 'AddCategory',
      component: AddCategory,
    },
    {
      // path: '/Category/:id',
      // path: '/Categories/:id',
      // name: 'Category',
      // component: Category,
    },
    {
      path: '/About',
      name: 'About',
      component: AboutView,
    },
  ],
})

export default router
