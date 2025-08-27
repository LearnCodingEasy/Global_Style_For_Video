<!-- في frontend: src/views/AuthCallback.vue -->
<template>
  <div class="auth-callback">
    <div v-if="loading" class="loading">
      <p>جاري تسجيل الدخول...</p>
    </div>
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button @click="redirectToLogin">العودة إلى تسجيل الدخول</button>
    </div>
    <div v-else class="success">
      <p>تم تسجيل الدخول بنجاح!</p>
      <p>جاري توجيهك إلى الصفحة الرئيسية...</p>
    </div>
  </div>
</template>

<script>
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

export default {
  name: 'AuthCallback',
  setup() {
    const userStore = useUserStore()
    const router = useRouter()

    return { userStore, router }
  },
  data() {
    return {
      loading: true,
      error: null,
    }
  },
  async mounted() {
    try {
      // استخراج البيانات من URL parameters
      const urlParams = new URLSearchParams(window.location.search)

      const tokens = {
        access: urlParams.get('access'),
        refresh: urlParams.get('refresh'),
        user_id: urlParams.get('user_id'),
        email: urlParams.get('email'),
        name: urlParams.get('name'),
        surname: urlParams.get('surname'),
        avatar: urlParams.get('avatar'),
      }

      // التحقق من وجود البيانات المطلوبة
      if (!tokens.access || !tokens.refresh) {
        throw new Error('بيانات التسجيل غير مكتملة')
      }

      // حفظ tokens في store
      this.userStore.setToken({
        access: tokens.access,
        refresh: tokens.refresh,
      })

      // حفظ بيانات المستخدم
      this.userStore.setUserInfo({
        id: tokens.user_id,
        email: tokens.email,
        name: tokens.name,
        surname: tokens.surname,
        get_avatar: tokens.avatar,
        is_online: true,
      })

      // الانتقال إلى الصفحة الرئيسية بعد ثانية
      setTimeout(() => {
        this.router.push('/')
      }, 1000)
    } catch (error) {
      console.error('❌ خطأ في تسجيل الدخول:', error)
      this.error = error.message
      this.loading = false
    }
  },
  methods: {
    redirectToLogin() {
      this.router.push('/login')
    },
  },
}
</script>

<style scoped>
.auth-callback {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  text-align: center;
}

.loading,
.error,
.success {
  padding: 2rem;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.error {
  color: #d32f2f;
}

.success {
  color: #2e7d32;
}
</style>
