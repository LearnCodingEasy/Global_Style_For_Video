<template>
  <div class="explain-page">
    <h2>Explain Details</h2>
    <!-- Loading -->
    <div v-if="loading" class="loading">Loading...</div>
    <!-- Data -->
    <div v-else-if="explain" class="card">
      <h3>{{ explain.name }}</h3>
      <p><strong>ID:</strong> {{ explain.id }}</p>
    </div>
    <!-- Not Found -->
    <div v-else class="empty">Explain not found</div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import explainService from '@/services/explainsService'

// =======================
// State
// =======================
const route = useRoute()
const explain = ref(null)
const loading = ref(true)

const fetchExplain = async () => {
  try {
    const { id } = route.params
    const data = await explainService.get(id)
    console.log('DETAIL DATA 👉', data)
    explain.value = data.data
  } catch (err) {
    console.log(err)
  } finally {
    loading.value = false
  }
}
watch(() => route.params.id, fetchExplain)

onMounted(fetchExplain)
</script>

<style scoped>
.explain-page {
  max-width: 600px;
  margin: auto;
}

.card {
  padding: 15px;
  border: 1px solid #ddd;
}

.loading {
  text-align: center;
}

.empty {
  color: #999;
  text-align: center;
}
</style>
