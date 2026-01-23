# Drag And Drop

## Install

```cmd
npm install @vue-flow/core
npm install @vue-flow/background
npm install @vue-flow/controls
npm install @vue-flow/minimap
npm install lodash
npm install @dagrejs/dagre
npm install vuedraggable@next
```

```cmd
npm install @vue-flow/core @vue-flow/background @vue-flow/controls @vue-flow/minimap vuedraggable@next lodash @dagrejs/dagre
```

## first Graph

```html
<template>
  <div class="Component-Name">
    <VueFlow v-model:nodes="nodes" v-model:edges="edges">
      <Background />
      <Controls />
      <MiniMap />
    </VueFlow>
  </div>
</template>
```

```js
<script setup>
import { ref } from 'vue'
import { VueFlow } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'

const nodes = ref([
  { id: '1', position: { x: 100, y: 80 }, data: { label: 'Start' } },
  { id: '2', position: { x: 300, y: 200 }, data: { label: 'End' } },
])

const edges = ref([{ id: 'e1-2', source: '1', target: '2' }])
</script>
```

```css
<style>
.vue-flow__node,
.vue-flow__node-custom {
  background: purple;
  color: white;
  border: 1px solid purple;
  border-radius: 4px;
  box-shadow: 0 0 0 1px purple;
  padding: 8px;
}
</style>
```

![This is an image](automation\first-graph.png)

## Title

```html
<template>
  <div class="Component-Name">
    <VueFlow
      v-model:nodes="nodes"
      v-model:edges="edges"
      @node-click="onNodeClick"
      @edge-click="onEdgeClick"
    >
      <Background />
      <Controls />
      <MiniMap />
    </VueFlow>
  </div>
</template>
```

```js
<script setup>
import { ref } from 'vue'
import { VueFlow } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'

const nodes = ref([
  { id: '1', position: { x: 100, y: 80 }, data: { label: 'Start' } },
  { id: '2', position: { x: 300, y: 200 }, data: { label: 'End' } },
])

const edges = ref([{ id: 'e1-2', source: '1', target: '2' }])
function onNodeClick(e) {
  console.log('Node Click:', e.node)
}
</script>
```

```css
<style>
.vue-flow__node,
.vue-flow__node-custom {
  background: purple;
  color: white;
  border: 1px solid purple;
  border-radius: 4px;
  box-shadow: 0 0 0 1px purple;
  padding: 8px;
}
</style>
```

![This is an image](automation\title.png)
