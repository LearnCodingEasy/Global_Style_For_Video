<script setup>
import { ref, onMounted } from 'vue'
import gsap from 'gsap'
const box = ref(null)
onMounted(() => {
  gsap.to(box.value, {
    x: 300,
    scale: 1.5,
    duration: 2,
  })
})
</script>
<template>
  <div class="container">
    <div ref="box" class="box">
      Lorem ipsum dolor, sit amet consectetur adipisicing elit. Ipsa, ab incidunt ipsum
      perspiciatis.
    </div>
  </div>
</template>
