<template>
  <div class="explain-page">
    <h2>Explain Create</h2>
    <div class="card">
      <input v-model="form.name" placeholder="Explain name" />
      <textarea
        v-model="form.description"
        name="form.description"
        id=""
        cols="10"
        rows="10"
        placeholder="Explain Description"
      ></textarea>
      <input type="email" v-model="form.email" />
      <input type="url" v-model="form.url" />
      <input type="number" v-model.number="form.price" />
      <input type="number" v-model.number="form.count" />
      <input type="number" v-model.number="form.views" />
      <input type="number" v-model.number="form.rating" />
      <input type="number" step="0.01" v-model="form.actual_price" />

      <input type="checkbox" v-model="form.is_active" />

      <input type="date" v-model="form.birth_date" />
      <input type="time" v-model="form.start_time" />

      <input type="file" @change="onFileChange" />

      <input type="file" accept="image/*" @change="onImageChange" />

      <div class="new_data">
        <label>settings [press alt + comma to add]:</label><br />
        <input
          type="text"
          v-model="tempSetting"
          @keyup.alt="addSetting"
          placeholder="Your Settings"
          class="w-full mt-2 py-2 px-4 border border-gray-200 rounded-lg"
        />
        <div class="grid_12 mt-4">
          <div class="">
            <span @click="deleteSetting(setting)" class="cursor-pointer">
              <prime_tag
                severity="success"
                v-for="setting in form.settings"
                :key="setting"
                class="mr-1"
              >
                <span @click="deleteSetting(setting)" class="item_1">
                  <prime_tag severity="success" :value="setting"> </prime_tag>
                </span>
              </prime_tag>
            </span>
          </div>
        </div>
      </div>

      <select v-model="form.category">
        <option value="">Choose a category</option>

        <option v-for="cat in categories" :key="cat.id" :value="cat.id">
          {{ cat.name }}
        </option>
      </select>

      <button @click="submit">Add</button>
    </div>
    <div v-if="toast.show" :class="['toast', toast.type]">{{ toast.message }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

import explainService from '@/services/explainsService'

// =======================
// State
// =======================
const form = ref({
  // Text
  name: '',
  description: '',
  email: '',
  url: '',

  // Number
  price: 0,
  count: 0,
  views: 0,
  rating: 0,
  actual_price: 0.0,

  // Boolean
  is_active: true,

  // Date Time
  birth_date: null,
  start_time: null,

  // Files & Image
  files: null,
  image: null,

  // Json
  settings: [],

  // 🔗 Foreign Key
  category: '',
})
const tempSetting = ref('')
const categories = ref([])

const toast = ref({
  show: false,
  message: '',
  type: 'success', // success | error
})
// =======================
// Helpers
// =======================
const showToast = (message, type = 'success') => {
  toast.value = { show: true, message, type }
  setTimeout(() => (toast.value.show = false), 3000)
}

// =======================
// Files
// =======================
const onFileChange = (e) => {
  form.value.files = e.target.files[0]
}
// =======================
// Images
// =======================
const onImageChange = (e) => {
  form.value.image = e.target.files[0]
}

// =======================
// Json
// =======================
const addSetting = (event) => {
  if (event.key === ',' && tempSetting.value.trim() !== '') {
    if (!form.value.settings.includes(tempSetting.value)) {
      form.value.settings.push(tempSetting.value)
    }
    tempSetting.value = ''
  }
}
const deleteSetting = (setting) => {
  form.value.settings = form.value.settings.filter((item) => {
    return setting !== item
  })
}

// =======================
// Category By Foreign Key
// =======================
onMounted(async () => {
  const res = await explainService.listExplainCategory()
  categories.value = res
  console.log('res.data: ', res)
})

// =======================
// API
// =======================

const submit = async () => {
  try {
    const formData = new FormData()

    // =================
    // Text
    // =================
    formData.append('name', form.value.name)

    formData.append('description', form.value.description)
    formData.append('email', form.value.email)
    formData.append('url', form.value.url)

    // =================
    // Numbers
    // =================
    formData.append('price', form.value.price)
    formData.append('count', form.value.count)
    formData.append('views', form.value.views)
    formData.append('rating', form.value.rating)
    formData.append('actual_price', form.value.actual_price)

    // =================
    // Boolean (مهم)
    // =================
    formData.append('is_active', form.value.is_active ? 'true' : 'false')

    // =================
    // Date / Time
    // =================
    if (form.value.birth_date) {
      formData.append('birth_date', form.value.birth_date)
    }

    if (form.value.start_time) {
      formData.append('start_time', form.value.start_time)
    }

    // =================
    // File
    // =================
    if (form.value.files) {
      formData.append('files', form.value.files)
      // ⚠️ الاسم لازم يطابق Django
    }

    // =================
    // Image
    // =================
    if (form.value.image) {
      formData.append('image', form.value.image)
    }

    // =================
    // JSON
    // =================
    formData.append('settings', JSON.stringify(form.value.settings))

    // =================
    // 🔗 Foreign Key
    // =================
    formData.append('category', form.value.category)
    await explainService.create(formData)
    showToast('Created successfully')
  } catch (err) {
    console.log('BACKEND ERROR 👉', err.response?.data || err)
    showToast('Operation failed', 'error')
  }
}
</script>

<style scoped>
.explain-page {
  max-width: 100%;
  margin: auto;
  padding: 2rem;
}
.card {
  padding: 15px;
  border: 1px solid #ddd;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
}
/* Toast */
.toast {
  position: fixed;
  top: 60px;
  right: 20px;
  padding: 12px 20px;
  color: white;
  border-radius: 5px;
  z-index: 1000;
}
.toast.success {
  background: #27ae60;
}
.toast.error {
  background: #c0392b;
}
</style>
