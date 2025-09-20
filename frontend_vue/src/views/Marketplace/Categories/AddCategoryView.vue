<template>
  <div class="Component-Name">
    <form @submit.prevent="submitFormVendor">
      <prime_card class="prime_card_form_login">
        <template #header>
          <div class="flex justify-between items-center w-full">
            <div class="text font-bold text-5xl">Add Category</div>
            <div class="image_logo">
              <!-- <img src="@/assets/Images/Messenger_80x80.png" alt="logo" /> -->
            </div>
          </div>
        </template>

        <template #content>
          <div class="">
            <div class="">
              <!-- Name -->
              <prime_fluid class="prime_card_form_login_content">
                <prime_input_text placeholder="Name" v-model="formLoginVendor.name" />
              </prime_fluid>
              <!-- Name -->
              <prime_fluid class="prime_card_form_login_content">
                <prime_input_text placeholder="Name" v-model="formLoginVendor.description" />
              </prime_fluid>
              <!-- ordering -->
              <prime_fluid class="prime_card_form_login_content">
                <prime_input_text placeholder="Name" v-model="formLoginVendor.ordering" />
              </prime_fluid>
              <!-- is_active -->
              <prime_fluid class="prime_card_form_login_content">
                <prime_input_text placeholder="Name" v-model="formLoginVendor.is_active" />
              </prime_fluid>
            </div>
          </div>
        </template>

        <template #footer>
          <button type="submit" class="btn_login mt-2 px-5 py-3 rounded">Log In</button>
        </template>
      </prime_card>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AddCategoryView',
  data() {
    return {
      formLoginVendor: {
        name: '',
        description: '',
        ordering: 0,
        is_active: true,
      },
      errorsLogin: [],
    }
  },
  methods: {
    async submitFormVendor() {
      this.errorsLogin = []

      if (!this.formLoginVendor.name) {
        this.$toast.add({
          severity: 'error',
          summary: 'Missing Data',
          detail: 'name and Password are required!',
          life: 3000,
        })
        return
      }

      try {
        const token = localStorage.getItem('access_token')

        const res = await axios.post(
          'http://localhost:8000/api/products/category/',
          this.formLoginVendor,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        )
        console.log('res: ', res)
        this.$toast.add({
          severity: 'success',
          summary: `Welcome Vendor`,
          detail: `${res.data.name}`,
          life: 3000,
        })
        this.$router.push('/products')
      } catch (err) {
        console.log('err: ', err)
        this.$toast.add({
          severity: 'error',
          summary: 'Login Failed',
          detail: 'name or password incorrect.',
          life: 3000,
        })
      }
    },
  },
  async mounted() {},
}
</script>
