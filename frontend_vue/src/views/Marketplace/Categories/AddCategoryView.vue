<template>
  <div class="Component-Name">
    <form @submit.prevent="submitFormCategory">
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
                <prime_input_text placeholder="Name" v-model="formCategory.name" />
              </prime_fluid>
              <!-- Name -->
              <prime_fluid class="prime_card_form_login_content">
                <prime_input_text placeholder="Name" v-model="formCategory.description" />
              </prime_fluid>
              <!-- ordering -->
              <prime_fluid class="prime_card_form_login_content">
                <prime_input_text placeholder="Name" v-model="formCategory.ordering" />
              </prime_fluid>
              <!-- is_active -->
              <prime_fluid class="prime_card_form_login_content">
                <prime_input_text placeholder="Name" v-model="formCategory.is_active" />
              </prime_fluid>
              <div
                class="new_data mobile_item_12 tablet_item_12 laptop_item_12 laptop_lg_item_12 desktop_item_6 desktop_lg_item_6"
              >
                <label for="websiteImage" class="font-semibold block my-2">Avatar</label>
                <prime_file_upload
                  type="file"
                  ref="fileAvatar"
                  :multiple="true"
                  name="demo[]"
                  @select="handleCategoryFileUpload"
                  accept="image/*"
                  :maxFileSize="1000000"
                >
                  <template #empty>
                    <span>Drag and drop files to here to upload.</span>
                  </template>
                </prime_file_upload>
              </div>
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
      formCategory: {
        name: '',
        description: '',
        ordering: 0,
        is_active: true,
        image: null,
      },
      selectedImageCategoryFile: null,
      errorsLogin: [],
    }
  },
  methods: {
    // For Upload Avatar Image to Post Store and for Post
    handleCategoryFileUpload(event) {
      const file = event.files ? event.files[0] : null
      if (file) {
        console.log('file: ', file)
        this.selectedImageCategoryFile = file
        this.formCategory.image = this.selectedImageCategoryFile
        console.log('FormData contains image:', this.selectedImageCategoryFile.name)
        // Send Image to View
        this.$toast.add({
          severity: 'success',
          summary: `Data contains image`,
          detail: `${this.selectedImageCategoryFile.name}`,
          life: 3000,
        })
      } else {
        console.log('No file selected.')
      }
    },
    async submitFormCategory() {
      this.errorsLogin = []
      let formData = new FormData()
      // Name
      if (!this.formCategory.name) {
        this.$toast.add({
          severity: 'error',
          summary: 'Missing Data',
          detail: 'Name Is Required!',
          life: 3000,
        })
        return
      } else {
        formData.append('name', this.formCategory.name)
      }
      // Description
      if (!this.formCategory.description) {
        this.$toast.add({
          severity: 'error',
          summary: 'Missing Data',
          detail: 'Description Is Required!',
          life: 3000,
        })
        return
      } else {
        formData.append('description', this.formCategory.description)
      }
      // Ordering
      if (!this.formCategory.ordering) {
        this.$toast.add({
          severity: 'error',
          summary: 'Missing Data',
          detail: 'Ordering Is Required!',
          life: 3000,
        })
        return
      } else {
        formData.append('ordering', this.formCategory.ordering)
      }
      // Is Active
      if (!this.formCategory.is_active) {
        this.$toast.add({
          severity: 'error',
          summary: 'Missing Data',
          detail: 'Is Active Is Required!',
          life: 3000,
        })
        return
      } else {
        formData.append('is_active', this.formCategory.is_active)
      }
      if (this.selectedImageCategoryFile) {
        // this.formCategory.append('image', this.selectedImageCategoryFile)
        // formData.append('image', this.selectedImageCategoryFile)
      }

      try {
        const token = localStorage.getItem('access_token')

        const res = await axios.post(
          'http://localhost:8000/api/products/category/',
          this.formCategory,
          // this.formData,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        )
        console.log('res: ', res)
        console.log('res: ', res.data)
        console.log('res: ', res.data.message)
        if (res.data.message == 'Category Created Successfully') {
          this.$toast.add({
            severity: 'success',
            summary: `Category Created`,
            detail: `${res.data.message}`,
            life: 3000,
          })
          this.$router.push('/products/')
        } else {
          this.toast.add({
            severity: 'error',
            summary: `Error Created Category`,
            detail: `Cent Add Category`,
            life: 3000,
          })
        }
      } catch (err) {
        console.log('err: ', err)
        this.$toast.add({
          severity: 'error',
          summary: 'Error Created Category Failed',
          detail: 'Error Created Category.',
          life: 3000,
        })
      }
    },
  },
  async mounted() {},
}
</script>
