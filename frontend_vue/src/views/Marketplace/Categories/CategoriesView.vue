<template>
  <div class="wrapper">
    <div class="container m-auto">
      <h2 class="text-center py-5 my-10 text-7xl text-capitalize">category:</h2>
      <div class="inner grid xxlg_grid_3 xlg_grid_3 laptop_lg_grid_2 md_grid_3 gap_20">
        <router-link class="class_name" to="AddCategory/"> Add </router-link>
        <router-link class="class_name" to="EditCategory/"> Edit </router-link>
        <div class="" v-if="loading">Data Loading</div>
        <div class="" v-else-if="error">{{ error }}</div>
        <prime_card v-else class="" v-for="cat in category" :key="cat.id">
          <template #header>
            <img alt="user header" :src="'http://localhost:8000/' + cat.get_thumbnail" />
          </template>
          <template #content>
            <div class="text font-bold text-5xl">{{ cat.name }}</div>
          </template>
          <template #footer>
            <router-link class="class_name" :to="`/category/${cat.id}`">
              <prime_button
                icon="pi pi-plus"
                label="Category Details"
                severity="info"
                @click="visible = true"
                class="class_name"
              />
            </router-link>
          </template>
        </prime_card>
      </div>
    </div>
  </div>
</template>
<!--

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
        console.log('res: ', res)
        this.category = res.data.data
        if (res.data.message == 'Categories List') {
          console.log('category: ', res.data.data)
        } else {
          console.log('category: ', res.data.message)
        }
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
-->

<script>
import categoryServices from '@/services/product_services'

export default {
  name: 'CategoriesView',
  data() {
    return {
      category: [],
      loading: false,
      error: null,
    }
  },
  computed: {},

  methods: {
    async allCategories() {
      try {
        this.loading = true
        const response = await categoryServices.allCategory()
        console.log('response: ', response)
        this.category = response.data.data
        console.log('response: ', response.data.data)
        if (response.data.message == 'Categories List') {
          console.log('category: ', response.data.data)
        } else {
          console.log('category: ', response.data.message)
        }
      } catch (err) {
        console.error('err: ', err)
        console.log('err: ', err)
        this.$toast.add({
          severity: 'error',
          summary: 'Failed To Load Category List',
          detail: err.message,
          life: 3000,
        })
      } finally {
        this.loading = false
        console.log('Finished loading categories ✅')
      }
    },
  },

  async mounted() {
    await this.allCategories()
  },
}
</script>



<style lang="scss" scoped></style>
