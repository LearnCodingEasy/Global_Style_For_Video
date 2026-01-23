<template>
  <div class="explain-details">
    <h2>Explain Details</h2>

    <div v-if="loading">Loading...</div>

    <div v-else>
      <p><strong>ID:</strong> {{ explain.id }}</p>
      <p><strong>Name:</strong> {{ explain.name }}</p>

      <button @click="goBack">Back</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import explainService from '@/services/explainsService'
import { watch } from 'vue'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const explain = ref({})

const fetchExplain = async () => {
  loading.value = true
  const res = await explainService.get(route.params.id)
  explain.value = res.data
  loading.value = false
}

const goBack = () => {
  router.push({ name: 'explains' })
}

onMounted(fetchExplain)
watch(() => route.params.id, fetchExplain)
</script>
