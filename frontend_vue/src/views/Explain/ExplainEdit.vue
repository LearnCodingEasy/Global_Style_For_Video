<template>
  <div class="explain-page">
    <h2>Explain Edit</h2>
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
      <input type="email" v-model="form.email" placeholder="Explain Email" />
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

      <button @click="submit">Update</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import explainService from '@/services/explainsService'

// =======================
// Router
// =======================
const route = useRoute()
const router = useRouter()

// =======================
// State
// =======================
const currentId = ref(null)
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
})

// =======================
// Get Explain By ID
// =======================
const getExplain = async () => {
  try {
    currentId.value = route.params.id
    const res = await explainService.get(currentId.value)
    form.value.name = res.data.name

    form.value.description = res.data.description
    form.value.email = res.data.email
    form.value.url = res.data.url
    form.value.price = res.data.price
    form.value.count = res.data.count
    form.value.views = res.data.views
    form.value.rating = res.data.rating
    form.value.actual_price = res.data.actual_price
    form.value.is_active = res.data.is_active
    form.value.birth_date = res.data.birth_date
    form.value.start_time = res.data.start_time
  } catch (err) {
    console.log('Get error:', err)
  }
}

// =======================
// Files
// =======================
const onFileChange = (e) => {
  form.value.files = e.target.files[0]
}

// =======================
// Update
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

    await explainService.update(currentId.value, formData)
    console.log('Updated Successfully')
    // لو حابب ترجع لليست
    router.push({ name: 'explains' })
  } catch (err) {
    console.log('Update error:', err)
  }
}

// =======================
// Lifecycle
// =======================
onMounted(() => {
  getExplain()
})
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
