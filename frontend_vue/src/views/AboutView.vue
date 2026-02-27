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
// function updateLabel() {
//   nodes.value[0].data.label = "Updated ✨"
// }
</script>

<template>
  <div class="VueFlow_Component_Name">
    <div class="">
      <button type="button" @click="addNode">Add Node</button>
      <!-- <button type="button" @click="updateLabel">Update Node Label</button> -->
    </div>
    <!-- eslint-disable vue/no-v-model-argument -->
    <VueFlow v-model:nodes="nodes" v-model:edges="edges" :default-zoom="1.5" :min-zoom="0.2" :max-zoom="5"
      @node-click="onNodeClick">
      <Background pattern-color="#aaa" :gap="8" />
      <MiniMap />
      <Controls />
    </VueFlow>
  </div>
</template>


<style lang="scss">
// Style For Explain
.VueFlow_Component_Name {
  height: 93vh;
  width: 90%;
  overflow: hidden;
  margin: auto;

  button {
    padding: 5px 10px;
    background-color: #ffeaa7;
    margin: 10px;
    border-radius: 5px;
    font-weight: bold;
    text-transform: capitalize;
  }
}

// Style For VueFlow
// Node Style
.vue-flow__node,
.vue-flow__node-custom {
  background: #ffeaa7;
  box-shadow: 0 0 0 1px #ffeaa7;
  padding: 8px;
  border: 1px solid #ffeaa7;
  border-radius: 4px;
  // font
  font-size: 15px;
  font-weight: bold;
  text-transform: capitalize;

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


<script>
export default { name: 'AboutView' }
</script>

<!--
// 📦 Drag and drop tools for the user interface
// import vuedraggable from 'vuedraggable'

// 3
function deleteLastNode() {
  nodes.value.pop()
}

// 4

// 🔹 اسم المفتاح في LocalStorage
/*
const STORAGE_KEY = "vueflow-workspace"
function save() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify({
    nodes: nodes.value,
    edges: edges.value
  }))
}
// Load All Data
function load() {
  const data = localStorage.getItem(STORAGE_KEY)
  if (data) {
    const parsed = JSON.parse(data)
    nodes.value = parsed.nodes
    edges.value = parsed.edges
  }
}

//
function onNodeClick() {
  nodes.value.push({
    id: Date.now().toString(),
    position: { x: 200, y: 200 },
    data: { label: "New Node 🚀" }
  })
}

//
function deleteNode(id) {
  nodes.value = nodes.value.filter(n => n.id !== id)
}
//
function exportJSON() {
  const data = localStorage.getItem(STORAGE_KEY)
  console.log("Exported JSON:", data)
}
function importJSON(json) {
  const parsed = JSON.parse(json)
  nodes.value = parsed.nodes
  edges.value = parsed.edges
}

watch([nodes, edges], save, { deep: true })

onMounted(load)

// 🔹 حفظ البيانات
function saveToLocal() {
  const data = {
    nodes: nodes.value,
    edges: edges.value
  }
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
}

// 🔹 تحميل البيانات
function loadFromLocal() {
  const data = localStorage.getItem(STORAGE_KEY)
  if (data) {
    const parsed = JSON.parse(data)
    nodes.value = parsed.nodes || []
    edges.value = parsed.edges || []
  }
}

// 🔹 مسح البيانات
function clearStorage() {
  localStorage.removeItem(STORAGE_KEY)
  nodes.value = []
  edges.value = []
}
*/

<script setup>
// استيراد المكتبات
import { ref, watch, onMounted } from 'vue'
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
  { id: '2', position: { x: 100, y: 200 }, data: { label: 'End' } },
])
// 🔗 Definition of Edges (Connecting Lines)
const edges = ref([{ id: 'e1-2', source: '1', target: '2' }])
// 🔹 اسم المفتاح في LocalStorage
/*
const STORAGE_KEY = "vueflow-workspace"
function save() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify({
    nodes: nodes.value,
    edges: edges.value
  }))
}
// Load All Data
function load() {
  const data = localStorage.getItem(STORAGE_KEY)
  if (data) {
    const parsed = JSON.parse(data)
    nodes.value = parsed.nodes
    edges.value = parsed.edges
  }
}

//
function onNodeClick() {
  nodes.value.push({
    id: Date.now().toString(),
    position: { x: 200, y: 200 },
    data: { label: "New Node 🚀" }
  })
}

//
function deleteNode(id) {
  nodes.value = nodes.value.filter(n => n.id !== id)
}
//
function exportJSON() {
  const data = localStorage.getItem(STORAGE_KEY)
  console.log("Exported JSON:", data)
}
function importJSON(json) {
  const parsed = JSON.parse(json)
  nodes.value = parsed.nodes
  edges.value = parsed.edges
}

watch([nodes, edges], save, { deep: true })

onMounted(load)
*/

/*
// 🔹 حفظ البيانات
function saveToLocal() {
  const data = {
    nodes: nodes.value,
    edges: edges.value
  }
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
}

// 🔹 تحميل البيانات
function loadFromLocal() {
  const data = localStorage.getItem(STORAGE_KEY)
  if (data) {
    const parsed = JSON.parse(data)
    nodes.value = parsed.nodes || []
    edges.value = parsed.edges || []
  }
}

// 🔹 مسح البيانات
function clearStorage() {
  localStorage.removeItem(STORAGE_KEY)
  nodes.value = []
  edges.value = []
}
🖱️ Clicking Node | print data in console.
function feature1() {
  console.log("Feature 1 Activated 🎯")
}
// 2
function addNode() {
  nodes.value.push({
    id: Date.now().toString(),
    position: { x: 200, y: 200 },
    data: { label: 'Dynamic Node 🚀' }
  })
}

// 3
function deleteLastNode() {
  nodes.value.pop()
}

// 4
function updateLabel() {
  nodes.value[0].data.label = "Updated ✨"
}

function onNodeClick(e) {
  deleteLastNode()
  updateLabel()
  addNode()
  feature1()
  console.log("Node Click:", e.node)
}
watch(
  [nodes, edges],
  () => {
    saveToLocal()
  },
  { deep: true }
)
*/
</script>

<script setup>
// 🔍 وإدارة الحالة Vue Flow تكامل

import { Panel } from '@vue-flow/core'
import { useVueFlow } from '@vue-flow/core'


//
//
//
//
//


// 2


// اتصال بين العقد والارتباطات 🌐
const { onConnect, addNodes, addEdges } = useVueFlow()

function addStep() {
  addNodes({
    id: String(Date.now()),
    position: { x: Math.random() * 200, y: Math.random() * 200 },
    data: { label: 'New Step' },
  })
}

// 4
import dagre from '@dagrejs/dagre'

function autoLayout() {
  const g = new dagre.graphlib.Graph()
  g.setGraph({ rankdir: 'LR' })

  nodes.value.forEach((node) => {
    g.setNode(node.id, { width: 150, height: 40 })
  })

  edges.value.forEach((edge) => {
    g.setEdge(edge.source, edge.target)
  })

  dagre.layout(g)

  g.nodes().forEach((id) => {
    const { x, y } = g.node(id)
    const node = nodes.value.find((n) => n.id === id)
    node.position = { x, y }
  })
}
</script>

<template>
  <div class="Component-Name">
    <VueFlow
      v-model:nodes="nodes"
      v-model:edges="edges"
      @node-click="onNodeClick"
      @edge-click="onEdgeClick"
      @connect="onConnect"
      :min-zoom="1"
      :max-zoom="2"
    >
      <h1 style="font-size: 40px; font-weight: bold">
        {{ currentWorkflowName }}
      </h1>
      <Background />
      <Controls />
      <MiniMap />
    </VueFlow>
  </div>
</template>

<style lang="scss">
/* Use a purple theme for our custom node */
.vue_flow_node_custom {
  background: purple;
  color: white;
  border: 1px solid purple;
  border-radius: 4px;
  box-shadow: 0 0 0 1px purple;
  padding: 8px;
}
.style_tow {
  background: #888888;
  color: #222;
  border: 1px solid #cfcece;
  border-radius: 4px;
  box-shadow: 0 0 0 1px #cfcece;
  padding: 8px;
}

div[data-class='tasksEle'] {
  // transition: all 0.3s linear;
  // overflow: hidden;
  // position: relative;
  counter-increment: counter;
  text-transform: capitalize;
  // width: max-content;
  min-width: 150px;
  max-width: 250px;
  text-align: left;
  cursor: pointer;
  &::after {
    content: counter(counter);
    position: absolute;
    color: #fff;
    font-weight: 700;
    right: 0px;
    top: 0;
    width: 20px;
    height: 28px;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #191e32;
    border-radius: 0px 0px 0px 5px;
  }
}


</style> -->
