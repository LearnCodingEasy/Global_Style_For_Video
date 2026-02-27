# Drag And Drop

<div dir="rtl">

Vue Flow علشان نعمل مخطط Nodes متوصلة ببعض (زي Workflow أو Automation Diagram).
<br/>
يعني عندك:
<br/>

🟡 Start
<br/>
⬇️
<br/>
🟡 End
<br/>

وخط بينهم 🔗

</div>

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

## First Graph

```html
<template>
  <div class="VueFlow_Component_Name">
    <!-- eslint-disable vue/no-v-model-argument -->
    <VueFlow v-model:nodes="nodes" v-model:edges="edges"> </VueFlow>
  </div>
</template>
```

```js
<script setup>
  import { ref } from 'vue'
  // VueFlow
  // 🔍 Vue Flow integration and state management
  import { VueFlow, } from "@vue-flow/core";
  // 🟣 Definition of Nodes
  const nodes = ref([
    { id: '1', position: { x: 100, y: 80 }, data: { label: 'Start' } },
    { id: '2', position: { x: 300, y: 200 }, data: { label: 'End' } },
  ])
  // 🔗 Definition of Edges (Connecting Lines)
  const edges = ref([{ id: 'e1-2', source: '1', target: '2' }])
</script>
```

```css
<style>
  /* Style For Explain */
  .VueFlow_Component_Name {
    height: 93vh;
    width: 90%;
    overflow: hidden;
    margin: auto;
  }
</style>
```

![This is an image](automation\first-graph.png)

## CSS Style

```html
<template>
  <div class="VueFlow_Component_Name">
    <!-- eslint-disable vue/no-v-model-argument -->
    <VueFlow v-model:nodes="nodes" v-model:edges="edges"> </VueFlow>
  </div>
</template>
```

```js
<script setup>
  import { ref } from 'vue'
  // VueFlow
  // 🔍 Vue Flow integration and state management
  import { VueFlow, } from "@vue-flow/core";
  // 🟣 Definition of Nodes
  const nodes = ref([
    { id: '1', position: { x: 100, y: 80 }, data: { label: 'Start' } },
    { id: '2', position: { x: 300, y: 200 }, data: { label: 'End' } },
  ])
  // 🔗 Definition of Edges (Connecting Lines)
  const edges = ref([{ id: 'e1-2', source: '1', target: '2' }])
</script>
```

```css
<style lang="scss">
  // Style For Explain
  .VueFlow_Component_Name {
    height: 93vh;
    width: 90%;
    overflow: hidden;
    margin: auto;
  }

  // Style For VueFlow
  // Node Style
  .vue-flow__node,
  .vue-flow__node-custom {
    background: #ffeaa7;
    color: white;
    box-shadow: 0 0 0 1px #ffeaa7;
    padding: 8px;
    border: 1px solid #ffeaa7;
    border-radius: 4px;
    font-size: 15px;
  }

  // Parent Single Node
  .vue-flow__node {
    border: 1px solid #ffeaa7;
    outline: none;
    &:focus-visible {
      border: 1px solid #ffeaa7;
    }
  }

  .vue-flow__node-default.selected,
  .vue-flow__node-default:focus,
  .vue-flow__node-default:focus-visible {
    border: 1px solid #ffeaa7;
  }

  // Edge
  .vue-flow__node-default .vue-flow__handle,
  .vue-flow__node-input .vue-flow__handle,
  .vue-flow__node-output .vue-flow__handle {
    width: 33px;
    height: 13px;
    border-radius: 10px;
    background-color: #fdcb6e;
    border: 1px solid transparent;
  }
</style>
```

![This is an image](automation\css_style.png)

## Background

```html
<template>
  <div class="VueFlow_Component_Name">
    <!-- eslint-disable vue/no-v-model-argument -->
    <VueFlow v-model:nodes="nodes" v-model:edges="edges">
      <Background />
      <Background pattern-color="#aaa" :gap="8" />
    </VueFlow>
  </div>
</template>
```

```js
<script setup>
  import { ref } from 'vue'
  // VueFlow
  // 🔍 Vue Flow integration and state management
  import { VueFlow, } from "@vue-flow/core";
  // 🖼️ Vue Flow: Adding a background to charts
  import { Background } from '@vue-flow/background'
  // 🟣 Definition of Nodes
  const nodes = ref([
    { id: '1', position: { x: 100, y: 80 }, data: { label: 'Start' } },
    { id: '2', position: { x: 300, y: 200 }, data: { label: 'End' } },
  ])
  // 🔗 Definition of Edges (Connecting Lines)
  const edges = ref([{ id: 'e1-2', source: '1', target: '2' }])
</script>
```

![This is an image](automation\Background.png)

## MiniMap

```html
<template>
  <div class="VueFlow_Component_Name">
    <!-- eslint-disable vue/no-v-model-argument -->
    <VueFlow v-model:nodes="nodes" v-model:edges="edges">
      <Background />
      <MiniMap />
    </VueFlow>
  </div>
</template>
```

```js
<script setup>
  import { ref } from 'vue'
  // VueFlow
  // 🔍 Vue Flow integration and state management
  import { VueFlow, } from "@vue-flow/core";
  // 🖼️ Vue Flow: Adding a background to charts
  import { Background } from '@vue-flow/background'
  // 🌍 Mini-map to view the app layout
  import { MiniMap } from '@vue-flow/minimap'
  // 🟣 Definition of Nodes
  const nodes = ref([
    { id: '1', position: { x: 100, y: 80 }, data: { label: 'Start' } },
    { id: '2', position: { x: 300, y: 200 }, data: { label: 'End' } },
  ])
  // 🔗 Definition of Edges (Connecting Lines)
  const edges = ref([{ id: 'e1-2', source: '1', target: '2' }])
</script>
```

![This is an image](automation\MiniMap.png)

## Controls

```html
<template>
  <div class="VueFlow_Component_Name">
    <!-- eslint-disable vue/no-v-model-argument -->
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
  // استيراد المكتبات
  import { ref } from 'vue'
  // VueFlow
  // 🔍 Vue Flow integration and state management
  import { VueFlow, } from "@vue-flow/core";
  // 🖼️ Vue Flow: Adding a background to charts
  import { Background } from '@vue-flow/background'
  // 🌍 Mini-map to view the app layout
  import { MiniMap } from '@vue-flow/minimap'
  // 🎛️ Controls for managing the chart state
  import { Controls } from '@vue-flow/controls'
  // 🟣 Definition of Nodes
  const nodes = ref([
    { id: '1', position: { x: 100, y: 80 }, data: { label: 'Start' } },
    { id: '2', position: { x: 100, y: 200 }, data: { label: 'End' } },
  ])
  // 🔗 Definition of Edges (Connecting Lines)
  const edges = ref([{ id: 'e1-2', source: '1', target: '2' }])
</script>

```

![This is an image](automation\Controls.png)

## Zoom

```html
<template>
  <div class="VueFlow_Component_Name">
    <!-- eslint-disable vue/no-v-model-argument -->
    <VueFlow
      v-model:nodes="nodes"
      v-model:edges="edges"
      :default-zoom="1.5"
      :min-zoom="0.2"
      :max-zoom="4"
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
  // استيراد المكتبات
  import { ref } from 'vue'
  // VueFlow
  // 🔍 Vue Flow integration and state management
  import { VueFlow, } from "@vue-flow/core";
  // 🖼️ Vue Flow: Adding a background to charts
  import { Background } from '@vue-flow/background'
  // 🌍 Mini-map to view the app layout
  import { MiniMap } from '@vue-flow/minimap'
  // 🎛️ Controls for managing the chart state
  import { Controls } from '@vue-flow/controls'
  // 🟣 Definition of Nodes
  const nodes = ref([
    { id: '1', position: { x: 100, y: 80 }, data: { label: 'Start' } },
    { id: '2', position: { x: 100, y: 200 }, data: { label: 'End' } },
  ])
  // 🔗 Definition of Edges (Connecting Lines)
  const edges = ref([{ id: 'e1-2', source: '1', target: '2' }])
</script>

```

![This is an image](automation\Zoom.png)

## Click Node

```html
<template>
  <div class="VueFlow_Component_Name">
    <!-- eslint-disable vue/no-v-model-argument -->
    <VueFlow
      v-model:nodes="nodes"
      v-model:edges="edges"
      @node-click="onNodeClick"
    >
      <Background pattern-color="#aaa" :gap="8" />
      <MiniMap />
      <Controls />
    </VueFlow>
  </div>
</template>
```

```js
<script setup>
  // استيراد المكتبات
  import { ref } from 'vue'
  // VueFlow
  // 🔍 Vue Flow integration and state management
  import { VueFlow, } from "@vue-flow/core";
  // 🖼️ Vue Flow: Adding a background to charts
  import { Background } from '@vue-flow/background'
  // 🌍 Mini-map to view the app layout
  import { MiniMap } from '@vue-flow/minimap'
  // 🎛️ Controls for managing the chart state
  import { Controls } from '@vue-flow/controls'
  // 📦 Drag and drop tools for the user interface
  // import vuedraggable from 'vuedraggable'
  // 🟣 Definition of Nodes
  const nodes = ref([
    {
      id: '1', position: { x: 100, y: 80 }, data: {
        label: "Start",
        type: "trigger",
        color: "green",
        apiUrl: "/start-process"
      }
    },
    { id: '2', position: { x: 100, y: 200 }, data: { label: 'End' } },
  ])
  // 🔗 Definition of Edges (Connecting Lines)
  const edges = ref([{ id: 'e1-2', source: '1', target: '2' }])
  // 🖱️ Clicking Node | print data in console.
  function onNodeClick(e) {
    console.log('Node Click:', e.node)
  }
</script>
```

### Add Node

```html
<template>
  <div class="VueFlow_Component_Name">
    <div class="">
      <button type="button" @click="addNode">Add Node</button>
    </div>
    <!-- eslint-disable vue/no-v-model-argument -->
    <VueFlow
      v-model:nodes="nodes"
      v-model:edges="edges"
      :default-zoom="1.5"
      :min-zoom="0.2"
      :max-zoom="5"
      @node-click="onNodeClick"
    >
      <Background pattern-color="#aaa" :gap="8" />
      <MiniMap />
      <Controls />
    </VueFlow>
  </div>
</template>
```

```js
<script setup>
  // استيراد المكتبات
  import { ref } from 'vue'
  // VueFlow
  // 🔍 Vue Flow integration and state management
  import { VueFlow, } from "@vue-flow/core";
  // 🖼️ Vue Flow: Adding a background to charts
  import { Background } from '@vue-flow/background'
  // 🌍 Mini-map to view the app layout
  import { MiniMap } from '@vue-flow/minimap'
  // 🎛️ Controls for managing the chart state
  import { Controls } from '@vue-flow/controls'
  // 🟣 Definition of Nodes
  const nodes = ref([
    {
      id: '1', position: { x: 100, y: 80 }, data: {
        label: "Start",
        type: "trigger",
        color: "green",
        apiUrl: "/start-process",
        ui: {
          theme: {
            background: '#0f172a',
            border: '#334155',
            shadow: '#334155'
          },
          layout: {
            width: 260,
            height: 240,
            rounded: true
          }
        },
        inputs: [
          { key: 'text', label: 'Text', type: 'string', value: '' },
          { key: 'delay', label: 'Delay (ms)', type: 'number', value: 0 },
          { key: 'color', label: 'Background Color', type: 'color', value: '#0f172a' }
        ],
        ai: {
          enabled: false,
          context: {},
          memory: [],
          suggestions: []
        }
      }
    },
    { id: '2', position: { x: 100, y: 150 }, data: { label: 'End' } },
  ])
  // 🔗 Definition of Edges (Connecting Lines)
  const edges = ref([{ id: 'e1-2', source: '1', target: '2' }])
  // 🖱️ Clicking Node | print data in console.
  function feature1() {
    console.log("Feature 1 Activated 🎯")
  }
  function onNodeClick(e) {
    feature1()
    console.log("Node Click:", e.node)
  }
  // ➕ Add Node
  function addNode() {
    nodes.value.push({
      id: Date.now().toString(),
      position: { x: 100, y: 220 },
      data: { label: 'Dynamic Node 🚀' }
    })
  }
</script>
```

![This is an image](automation\MiniMap.png)

### Update

```html

```

```js
<script setup>
  // استيراد المكتبات
  import { ref } from 'vue'
  // VueFlow
  // 🔍 Vue Flow integration and state management
  import { VueFlow, } from "@vue-flow/core";
  // 🖼️ Vue Flow: Adding a background to charts
  import { Background } from '@vue-flow/background'
  // 🌍 Mini-map to view the app layout
  import { MiniMap } from '@vue-flow/minimap'
  // 🎛️ Controls for managing the chart state
  import { Controls } from '@vue-flow/controls'
  // 🟣 Definition of Nodes
  const nodes = ref([
    {
      id: '1', position: { x: 100, y: 80 }, data: {
        label: "Start",
        type: "trigger",
        color: "green",
        apiUrl: "/start-process",
        ui: {
          theme: {
            background: '#0f172a',
            border: '#334155',
            shadow: '#334155'
          },
          layout: {
            width: 260,
            height: 240,
            rounded: true
          }
        },
        inputs: [
          { key: 'text', label: 'Text', type: 'string', value: '' },
          { key: 'delay', label: 'Delay (ms)', type: 'number', value: 0 },
          { key: 'color', label: 'Background Color', type: 'color', value: '#0f172a' }
        ],
        ai: {
          enabled: false,
          context: {},
          memory: [],
          suggestions: []
        }
      }
    },
    { id: '2', position: { x: 100, y: 150 }, data: { label: 'End' } },
  ])
  // 🔗 Definition of Edges (Connecting Lines)
  const edges = ref([{ id: 'e1-2', source: '1', target: '2' }])
  // 🖱️ Clicking Node | print data in console.
  function feature1() {
    console.log("Feature 1 Activated 🎯")
  }
  function onNodeClick(e) {
    feature1()
    console.log("Node Click:", e.node)
  }
  // ➕ Add Node
  function addNode() {
    nodes.value.push({
      id: Date.now().toString(),
      position: { x: 100, y: 220 },
      data: { label: 'Dynamic Node 🚀' }
    })
  }
  // ♻️ Update Node
  function updateLabel() {
    nodes.value[0].data.label = "Updated ✨"
  }
</script>
```

### Install

```html

```

```js

```

### Install

```html

```

```js

```

### Install

```html

```

```js

```

### Install

```html

```

```js

```

## Install

```html

```

```js

```

## Install

```html

```

```js

```

## Install

```html

```

```js

```

## Install

```html

```

```js

```

## Install

```html

```

```js

```

## Install

```html

```

```js

```

## Install

```html

```

```js

```

## Install

```html

```

```js

```

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
// VueFlow
// 🔍 Vue Flow integration and state management
import { VueFlow } from '@vue-flow/core'
// 🖼️ Vue Flow إضافة خلفية لمخططات
import { Background } from '@vue-flow/background'
// 🎛️ عناصر تحكم لتحكم في حالة المخطط
import { Controls } from '@vue-flow/controls'
// 🌍 خريطة مصغرة لرؤية مخطط التطبيق
import { MiniMap } from '@vue-flow/minimap'
// 🟣 Definition of Nodes
const nodes = ref([
  { id: '1', position: { x: 100, y: 80 }, data: { label: 'Start' } },
  { id: '2', position: { x: 300, y: 200 }, data: { label: 'End' } },
])
// 🔗 Definition of Edges (Connecting Lines)
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
