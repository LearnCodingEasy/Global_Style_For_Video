<!-- <template>
  <div class="container m-auto">
    <form @submit.prevent="submitFormSignup">
      <prime_card class="prime_card_form_signup">
        <template #header>
          <div class="flex justify-between items-center w-full">
            <div class="text font-bold text-5xl text-center">Vendors</div>
          </div>
        </template>

        <template #content>
          <div class="" v-for="Vendor in Vendors" :key="Vendor.id">
            {{ Vendor.name }}
          </div>
          <prime_fluid class="prime_card_form_signup_content">
            <div class="flex gap-2">
              <prime_input_text placeholder="First name" v-model="formSignup.name" />
            </div>
          </prime_fluid>
        </template>

        <template #footer>
          <button type="submit" class="btn_signup mt-2 px-5 py-3 rounded border-y-indigo-950">
            Become Vendor Signup
          </button>
        </template>
      </prime_card>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Vendors',
  data() {
    return {
      Vendors: [],
      formSignup: {
        name: '',
      },

      errorsSignup: [],
    }
  },
  methods: {
    async submitFormSignup() {
      this.errorsSignup = []

      if (!this.formSignup.name) {
        this.errorsSignup.push('Please fill all required fields')
      }

      if (this.errorsSignup.length > 0) {
        this.$toast.add({
          severity: 'error',
          summary: 'Validation Error',
          detail: this.errorsSignup.join(', '),
          life: 4000,
        })
        return
      }

      try {
        // http://127.0.0.1:8000
        const res = await axios.post('/api/vendors/', this.formSignup)
        if (res.data.message === 'success') {
          this.$toast.add({
            severity: 'success',
            summary: 'User Registered',
            detail: 'Check your name to activate your account.',
            life: 3000,
          })
        }
      } catch (err) {
        this.$toast.add({
          severity: 'error',
          summary: 'Signup Failed',
          detail: err.message,
          life: 3000,
        })
      }
    },
  },
}
</script>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const backgrounds = ref([])
const name = ref(null)

const fetchBackgrounds = async () => {
  const res = await axios.get('http://localhost:8000/api/vendors/')
  backgrounds.value = res.data
  console.log('backgrounds.value: ', backgrounds.value)
}

// const submitFormSignup = async () => {
//   const formData = new FormData()
//   formData.append('name', name.value)

//   await axios.post('http://localhost:8000/api/vendors/', formData, {
//     headers: {
//       'Content-Type': 'multipart/form-data',
//     },
//   })

//   fetchBackgrounds()
// }

onMounted(() => {
  fetchBackgrounds()
})
</script> -->

<template>
  <div class="wrapper">
    <div class="container m-auto">
      <h2 class="text-center py-5 my-10 text-7xl text-capitalize">Vendors</h2>
      <div
        class="inner grid xxlg_grid_3 xlg_grid_3 laptop_lg_grid_2 md_grid_3 gap_20"
        v-if="vendors.length != []"
      >
        <!-- <div class="" v-if="vendors != []"> -->
        <prime_card class="" v-for="vendor in vendors" :key="vendor.id">
          <template #header>
            <div class="flex justify-between items-center w-full">
              <div class="text font-bold text-5xl text-center">
                {{ vendor.name }}
              </div>
            </div>
          </template>

          <template #content>
            <div class="">
              {{ vendor.name }}
            </div>
          </template>

          <template #footer>
            <router-link class="class_name" :to="'Vendors/' + vendor.id">
              Show Vendor Details
            </router-link>
          </template>
        </prime_card>
      </div>
      <div class="" v-else>
        <h2>Become Vendor</h2>
        <AddVendor></AddVendor>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import AddVendor from '../../components/Marketplace/AddVendor.vue'

export default {
  name: 'VendorsView',
  data() {
    return {
      vendors: [],
    }
  },
  methods: {
    async getVendors() {
      try {
        const res = await axios.get('http://localhost:8000/api/vendors/')

        console.log('res.data: ', res.data)
        this.vendors = res.data.data
        console.log('this.vendors: ', this.vendors)
        if (this.vendors != this.vendors) {
          this.$toast.add({
            severity: 'success',
            summary: `Welcome Vendor`,
            detail: `${res.data.name}`,
            life: 3000,
          })
        }
      } catch (err) {
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
    await this.getVendors()
  },
  components: {
    AddVendor,
  },
}
</script>

<!-- <script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const backgrounds = ref([])
const name = ref(null)

const fetchBackgrounds = async () => {
  const res = await axios.get('http://localhost:8000/api/vendors/')
  backgrounds.value = res.data
  console.log('backgrounds.value: ', backgrounds.value)
}

// const submitFormSignup = async () => {
//   const formData = new FormData()
//   formData.append('name', name.value)

//   await axios.post('http://localhost:8000/api/vendors/', formData, {
//     headers: {
//       'Content-Type': 'multipart/form-data',
//     },
//   })

//   fetchBackgrounds()
// }

onMounted(() => {
  fetchBackgrounds()
})
</script> -->
