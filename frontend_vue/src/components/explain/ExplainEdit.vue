<template>
  <div class="card">
    <input v-model="localName" />
    <button @click="update" :disabled="loading">Update</button>
    <button @click="$emit('cancel')" class="cancel">Cancel</button>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: String,
  loading: Boolean,
})

const emit = defineEmits(['update', 'cancel'])

const localName = ref(props.modelValue)

watch(
  () => props.modelValue,
  (val) => (localName.value = val),
)

const update = () => {
  emit('update', { name: localName.value })
}
</script>
