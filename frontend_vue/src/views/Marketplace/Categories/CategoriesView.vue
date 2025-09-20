<template>
  <div class="wrapper">
    <div class="container m-auto">
      <div class="inner grid xxlg_grid_3 xlg_grid_3 laptop_lg_grid_2 md_grid_3 gap_20">
        <router-link class="class_name" to="AddCategoryView/"> Add </router-link>

        <prime_card class="" v-for="cat in category" :key="cat.id">
          <template #header>
            <div class="flex justify-between items-center w-full">
              <div class="text font-bold text-5xl text-center">category</div>
            </div>
          </template>

          <template #content>
            <div class="">
              {{ cat.name }}
            </div>
          </template>
          <template #footer>
            <router-link class="class_name" :to="cat.id"> Show Vendor Details </router-link>
          </template>
        </prime_card>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CategoriesView',

  data() {
    return {
      category: [],
    }
  },
  methods: {
    async getCategory() {
      try {
        const res = await axios.get('http://localhost:8000/api/products/category/')
        console.log('category: ', res.data)
        this.category = res.data
      } catch (err) {
        this.$toast.add({
          severity: 'error',
          summary: 'category Failed',
          detail: err.message,
          life: 3000,
        })
      }
    },
  },
  async mounted() {
    await this.getCategory()
  },
}
</script>

<style lang="scss" scoped></style>
