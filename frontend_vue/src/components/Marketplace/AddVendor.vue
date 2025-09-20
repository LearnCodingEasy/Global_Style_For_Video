<template>
  <div class="Component-Name">
    <form @submit.prevent="submitFormVendor">
      <prime_card class="prime_card_form_login">
        <template #header>
          <div class="flex justify-between items-center w-full">
            <div class="text font-bold text-5xl">Log in vendor</div>
            <div class="image_logo">
              <!-- <img src="@/assets/Images/Messenger_80x80.png" alt="logo" /> -->
            </div>
          </div>
        </template>

        <template #content>
          <prime_fluid class="prime_card_form_login_content">
            <!-- Name -->
            <prime_input_text placeholder="Name" v-model="formLoginVendor.name" />
          </prime_fluid>
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
  name: 'AddVendorView',
  data() {
    return {
      formLoginVendor: {
        name: '',
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
        const res = await axios.post('http://localhost:8000/api/vendors/', this.formLoginVendor)
        console.log('res: ', res)
        this.$toast.add({
          severity: 'success',
          summary: `Welcome Vendor`,
          detail: `${res.data.name}`,
          life: 3000,
        })
        this.$router.push('/')
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
