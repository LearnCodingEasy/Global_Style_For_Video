<template>
  <div class="wrapper">
    <div class="container m-auto">
      <div class="inner grid xxlg_grid_3 xlg_grid_3 laptop_lg_grid_2 md_grid_3 gap_20">
        <div class="">
          <prime_card class="">
            <template #header>
              <div class="flex justify-between items-center w-full">
                <div class="text font-bold text-5xl text-center">Vendor Details</div>
              </div>
            </template>

            <template #content>
              <div class="">
                {{ vendor.name }}
              </div>
            </template>

            <template #footer>
              <router-link :to="{ name: 'EditVendor', props: { id: vendor.id } }">edit</router-link>
            </template>
          </prime_card>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'VendorView',
  data() {
    return {
      vendor: {},
    }
  },
  methods: {
    async getVendor() {
      try {
        const vendorId = this.$route.params.id
        const res = await axios.get(`http://localhost:8000/api/vendors/${vendorId}`)
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
  },
  async mounted() {
    await this.getVendor()
  },
}
</script>
