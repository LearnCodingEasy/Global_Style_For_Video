<template>
  <div class="wrapper">
    <div class="container m-auto">
      <div class="inner grid xxlg_grid_3 xlg_grid_3 laptop_lg_grid_2 md_grid_3 gap_20">
        <prime_card class="" v-for="product in products" :key="product.id">
          <template #header>
            <div class="flex justify-between items-center w-full">
              <div class="text font-bold text-5xl text-center">products</div>
            </div>
          </template>

          <template #content>
            <div class="">
              {{ product.name }}
            </div>
          </template>

          <template #footer>
            <prime_button
              icon="pi pi-plus"
              label="Show Vendor Details"
              severity="info"
              @click="visible = true"
              class="class_name"
              :to="product.id"
            />
          </template>
        </prime_card>
      </div>
      <div class="inner grid xxlg_grid_3 xlg_grid_3 laptop_lg_grid_2 md_grid_3 gap_20">
        <Categories></Categories>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Categories from './Categories/CategoriesView.vue'

export default {
  name: 'ProductsView',

  data() {
    return {
      products: [],
    }
  },
  methods: {
    async getProducts() {
      try {
        const res = await axios.get('http://localhost:8000/api/products/product/')
        console.log('products: ', res.data)
        this.products = res.data
      } catch (err) {
        this.$toast.add({
          severity: 'error',
          summary: 'products Failed',
          detail: err.message,
          life: 3000,
        })
      }
    },
  },
  async mounted() {
    await this.getProducts()
  },
  components: {
    Categories,
  },
}
</script>

<style lang="scss" scoped></style>
