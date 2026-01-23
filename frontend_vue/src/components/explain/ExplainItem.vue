<template>
  <div class="item">
    <RouterLink :to="{ name: 'explain-details', params: { id: item.id } }">
      <span class="name">
        {{ item.name }}
      </span>
    </RouterLink>

    <div class="actions">
      <button @click="$emit('edit', item)">Edit</button>
      <ExplainDelete @delete="$emit('delete', item.id)" />
    </div>
  </div>
</template>

<script setup>
import ExplainDelete from './ExplainDelete.vue'

defineProps({
  item: Object,
})
</script>
