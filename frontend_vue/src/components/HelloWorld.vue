<!-- <script setup>
defineProps({
  msg: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <div class="greetings">
    <h1 class="green">{{ msg }}</h1>
    <h3>
      You’ve successfully created a project with
      <a href="https://vite.dev/" target="_blank" rel="noopener">Vite</a> +
      <a href="https://vuejs.org/" target="_blank" rel="noopener">Vue 3</a>.
    </h3>
  </div>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style> -->
<template>
  <div class="app" dir="rtl" lang="ar">
    <IntroScreen v-if="!started" @start="onStart" />

    <template v-else>
      <StoryProgress :current="currentScene" :total="totalScenes" />
      <AudioController :enabled="started" />

      <main>
        <Scene01Greeting @enter="setCurrent" />
        <Scene02Hesitation @enter="setCurrent" />
        <Scene03Identity @enter="setCurrent" />
        <Scene04Journey @enter="setCurrent" />
        <Scene05Message @enter="setCurrent" />
        <Scene06Purpose @enter="setCurrent" />
        <Scene07Boundaries @enter="setCurrent" />
        <Scene08Learning @enter="setCurrent" />
        <Scene09Vulnerability @enter="setCurrent" />
        <Scene10Respect @enter="setCurrent" />
        <Scene11TimeAndPlace @enter="setCurrent" />
        <Scene12Ending @enter="setCurrent" />
      </main>
    </template>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import IntroScreen from './components/IntroScreen.vue'
import StoryProgress from './components/StoryProgress.vue'
import AudioController from './components/AudioController.vue'

import Scene01Greeting from './scenes/Scene01Greeting.vue'
import Scene02Hesitation from './scenes/Scene02Hesitation.vue'
import Scene03Identity from './scenes/Scene03Identity.vue'
import Scene04Journey from './scenes/Scene04Journey.vue'
import Scene05Message from './scenes/Scene05Message.vue'
import Scene06Purpose from './scenes/Scene06Purpose.vue'
import Scene07Boundaries from './scenes/Scene07Boundaries.vue'
import Scene08Learning from './scenes/Scene08Learning.vue'
import Scene09Vulnerability from './scenes/Scene09Vulnerability.vue'
import Scene10Respect from './scenes/Scene10Respect.vue'
import Scene11TimeAndPlace from './scenes/Scene11TimeAndPlace.vue'
import Scene12Ending from './scenes/Scene12Ending.vue'

import { totalScenes } from './data/story.js'

const started = ref(false)
const currentScene = ref(1)

function onStart() {
  started.value = true
}

function setCurrent(id) {
  currentScene.value = id
}
</script>

<style scoped>
.app {
  position: relative;
  width: 100%;
}

main {
  position: relative;
  width: 100%;
}
</style>
