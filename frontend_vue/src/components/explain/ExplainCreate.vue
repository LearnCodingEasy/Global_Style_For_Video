<template>
  <div class="">
    <div class="card">
      <input v-model="name" placeholder="Explain name" />
      <button @click="create" :disabled="loading">Add</button>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['created'])

defineProps({
  loading: Boolean,
})

const name = ref('')
const error = ref('')

const create = () => {
  if (!name.value.trim()) {
    error.value = 'Name is required'
    return
  }

  emit('created', { name: name.value })
  name.value = ''
  error.value = ''
}
</script>
