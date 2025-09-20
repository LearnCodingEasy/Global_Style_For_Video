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
            <prime_input_text placeholder="Name" v-model="vendor.name" />
          </prime_fluid>
        </template>

        <template #footer>
          <button type="submit" class="btn_login mt-2 px-5 py-3 rounded">Edit Vendors</button>
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
      vendor: {},
      errorsLogin: [],
    }
  },
  async mounted() {
    await this.getVendor()
  },
  methods: {
    async getVendor() {
      try {
        const vendorId = this.$route.params.id
        const res = await axios.get(`http://localhost:8000/api/vendors/${vendorId}/`)
        console.log('vendor: ', res.data)
        this.vendor = res.data
        this.$toast.add({
          severity: 'success',
          summary: `Welcome Vendor`,
          detail: `${res.data.name}`,
          life: 3000,
        })
      } catch (err) {
        console.log('err: ', err)
        console.log('err.message: ', err.message)
        this.$toast.add({
          severity: 'error',
          summary: 'Signup Failed',
          detail: err.message,
          life: 3000,
        })
      }
    },
    async submitFormVendor() {
      this.errorsLogin = []

      if (!this.vendor.name) {
        this.$toast.add({
          severity: 'error',
          summary: 'Missing Data',
          detail: 'name and Password are required!',
          life: 3000,
        })
        return
      }

      try {
        const vendorId = this.$route.params.id

        const res = await axios.post(`http://localhost:8000/api/vendors/${vendorId}/`, this.vendor)
        console.log('res: ', res)
        this.$toast.add({
          severity: 'success',
          summary: `Welcome Vendor`,
          detail: `${res.data.name}`,
          life: 3000,
        })
        // this.$router.push('/')
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
}
</script>
