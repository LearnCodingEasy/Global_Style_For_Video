<!-- All Data -->
<template>
  <div class="explain-page">
    <h2>Explain Manager</h2>
    <div class="list">
      <div class="item">
        <RouterLink to="/explains/explain_create"> explain_create </RouterLink>
      </div>

      <div class="item" v-for="item in explains" :key="item.id">
        <RouterLink :to="{ name: 'explain-details', params: { id: item.id } }">
          <div style="text-transform: capitalize">name :{{ item.name }}</div>
          <div>description: {{ item.description }}</div>
          <div>email :{{ item.email }}</div>
          <div>url :{{ item.url }}</div>
          <div>price :{{ item.price }}</div>
          <div>count :{{ item.count }}</div>
          <div>views :{{ item.views }}</div>
          <div>rating :{{ item.rating }}</div>
          <div>actual_price :{{ item.actual_price }}</div>
          <div>is_active :{{ item.is_active }}</div>
          <div>birth_date :{{ item.birth_date }}</div>
          <div>start_time :{{ item.start_time }}</div>
          <div>created_at :{{ item.created_at }}</div>
          <div>updated_at :{{ item.updated_at }}</div>
          <div>files :{{ item.files }}</div>
          <div>image :{{ item.image }}</div>
          <div>
            <div class="">settings :</div>
            <span v-for="setting in item.settings" :key="setting" style="display: block">
              {{ setting }}
            </span>
          </div>
          <div>category Foreign Key :{{ item.category }}</div>
          <div>category Foreign Key Name:{{ item.category_name }}</div>
        </RouterLink>
        <RouterLink :to="{ name: 'explain_edit', params: { id: item.id } }">
          <span>Edit</span>
        </RouterLink>
        <button type="button" @click="remove(item.id)">Delete</button>
      </div>
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
const explains = ref([])
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
// API
// =======================
const fetchExplains = async () => {
  try {
    const data = await explainService.list()
    console.log('STORE DATA 👉', data)
    explains.value = data
  } catch (err) {
    console.log(err)
  }
}

const remove = async (id) => {
  if (!confirm('Delete this item?')) return
  try {
    await explainService.delete(id)
    showToast('Delete successfully')
    fetchExplains()
  } catch {
    console.log(`No`)
  } finally {
    console.log(`Yes`)
  }
}
onMounted(fetchExplains)
</script>

<style scoped>
.explain-page {
  max-width: 98%;
  margin: auto;
}
.card {
  display: flex;
  gap: 10px;
  margin-bottom: 5px;
}
input {
  flex: 1;
  padding: 8px;
}
button {
  padding: 8px 12px;
}
.cancel {
  background: #aaa;
}
.error {
  color: #c0392b;
  font-size: 14px;
}
.loader {
  text-align: center;
  margin: 20px;
}
.list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.item {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  border: 1px solid #ddd;
}
.actions {
  display: flex;
  gap: 10px;
}
.danger {
  background: #c0392b;
  color: white;
}
.pagination {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 20px;
}
/* Toast */
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 12px 20px;
  color: white;
  border-radius: 5px;
}
.toast.success {
  background: #27ae60;
}
.toast.error {
  background: #c0392b;
}
</style>

<!--

<template>
  <div class="explain-page">

    <div class="card">
      <input v-model="form.name" placeholder="Explain name" />
      <button @click="submit" :disabled="loading">
        {{ editMode ? 'Update' : 'Add' }}
      </button>
      <button v-if="editMode" @click="resetForm" class="cancel">Cancel</button>
    </div>
    <p v-if="errors.name" class="error">{{ errors.name }}</p>


    <div class="pagination">
      <button @click="prevPage" :disabled="page === 1">Prev</button>
      <span>Page {{ page }}</span>
      <button @click="nextPage" :disabled="!hasNext">Next</button>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'

const page = ref(1)
const pageSize = 10
const hasNext = ref(false)
const editMode = ref(false)


const errors = ref({
  name: '',
})


// =======================
// Helpers
// =======================

const validate = () => {
  errors.value.name = ''
  if (!form.value.name.trim()) {
    errors.value.name = 'Name is required'
    return false
  }
  return true
}
// =======================
// API
// =======================
const submit = async () => {
  if (!validate()) return
  loading.value = true
  try {
    if (editMode.value) {
      await explainService.update(currentId.value, form.value)
      showToast('Updated successfully')
    } else {
      await explainService.create(form.value)
      showToast('Created successfully')
    }
    resetForm()
    fetchExplains()
  } catch (err) {
    console.log('err: ', err)
    showToast('Operation failed', 'error')
  } finally {
    loading.value = false
  }
}
const editItem = (item) => {
  editMode.value = true
  currentId.value = item.id
  form.value.name = item.name
}

const resetForm = () => {
  editMode.value = false
  currentId.value = null
  form.value.name = ''
  errors.value.name = ''
}
// =======================
// Pagination
// =======================
const nextPage = () => {
  page.value++
  fetchExplains()
}
const prevPage = () => {
  page.value--
  fetchExplains()
}
// =======================
// Lifecycle
// =======================
onMounted(fetchExplains)
</script>

-->

<!-- <template>
  <div class="explain-page">
    <h2>Explain Manager</h2>


    <ExplainCreate v-if="!editMode" :loading="loading" @created="createExplain" />

    <ExplainEdit
      v-else
      :modelValue="form.name"
      :loading="loading"
      @update="updateExplain"
      @cancel="resetForm"
    />

    <div v-if="loading" class="loader">Loading...</div>

    <div v-else class="list">
      <ExplainItem
        v-for="item in explains"
        :key="item.id"
        :item="item"
        @edit="editItem"
        @delete="deleteExplain"
      />
    </div>

    <div class="pagination">
      <button @click="prevPage" :disabled="page === 1">Prev</button>
      <span>Page {{ page }}</span>
      <button @click="nextPage" :disabled="!hasNext">Next</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import explainService from '@/services/explainsService'

import ExplainCreate from '@/components/explain/ExplainCreate.vue'
import ExplainEdit from '@/components/explain/ExplainEdit.vue'
import ExplainItem from '@/components/explain/ExplainItem.vue'

// ================= State =================
const explains = ref([])
const loading = ref(false)

const page = ref(1)
const pageSize = 10
const hasNext = ref(false)

const editMode = ref(false)
const currentId = ref(null)

const form = ref({ name: '' })

const toast = ref({
  show: false,
  message: '',
  type: 'success',
})

// ================= Helpers =================
const showToast = (msg, type = 'success') => {
  toast.value = { show: true, message: msg, type }
  setTimeout(() => (toast.value.show = false), 3000)
}

// ================= API =================
const fetchExplains = async () => {
  loading.value = true
  const res = await explainService.list({
    params: { page: page.value, page_size: pageSize },
  })
  explains.value = res.data.results
  hasNext.value = !!res.data.next
  loading.value = false
}

const createExplain = async (data) => {
  loading.value = true
  await explainService.create(data)
  showToast('Created successfully')
  fetchExplains()
}

const updateExplain = async (data) => {
  loading.value = true
  await explainService.update(currentId.value, data)
  showToast('Updated successfully')
  resetForm()
  fetchExplains()
}

const deleteExplain = async (id) => {
  loading.value = true
  await explainService.delete(id)
  showToast('Deleted successfully')
  fetchExplains()
}

// ================= UI =================
const editItem = (item) => {
  editMode.value = true
  currentId.value = item.id
  form.value.name = item.name
}

const resetForm = () => {
  editMode.value = false
  currentId.value = null
  form.value.name = ''
}

// ================= Pagination =================
const nextPage = () => {
  page.value++
  fetchExplains()
}
const prevPage = () => {
  page.value--
  fetchExplains()
}

onMounted(fetchExplains)

 -->
