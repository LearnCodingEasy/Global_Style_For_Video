<template>
  <button @click="confirmDelete" class="danger">Delete</button>
</template>

<script setup>
const emit = defineEmits(['delete'])

const confirmDelete = () => {
  if (confirm('Delete this item?')) {
    emit('delete')
  }
}
</script>
