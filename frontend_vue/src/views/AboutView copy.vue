<script setup>
// ===================================================
// 📦 1️⃣ Imports (المكتبات المستخدمة)
// ===================================================
// 🧠 Vue Composition API
import { ref, onMounted, watch } from 'vue'
// 🔗 VueFlow (المكتبة الأساسية للرسم والـ Drag & Drop)
import { VueFlow } from "@vue-flow/core"
// 🎨 خلفية الشبكة (Grid Background)
import { Background } from '@vue-flow/background'
// 🗺️ MiniMap (خريطة مصغرة للمخطط)
import { MiniMap } from '@vue-flow/minimap'
// 🎛️ Controls (Zoom / Fit / Lock)
import { Controls } from '@vue-flow/controls'
// 📦 Panel (لو عايز تضيف أزرار مخصصة داخل VueFlow)
import { Panel } from '@vue-flow/core'
// 🆔 إنشاء ID فريد لكل Node أو Edge
import { nanoid } from 'nanoid'
// ⏳ Debounce (يمنع الحفظ كل مرة يحصل تغيير سريع)
import debounce from 'lodash/debounce'
// 💾 Service مسؤول عن التخزين في LocalStorage
// =============================
// 📦 Imports
// =============================
import { onUnmounted, nextTick } from 'vue'
// VueFlow
// 🔍 Vue Flow integration and state management
// It gives you control tools (Zoom / Fit)
import { useVueFlow, } from "@vue-flow/core";
// 🖼️ Vue Flow: Adding a background to charts
// 🌍 Mini-map to view the app layout
// 🎛️ Controls for managing the chart state
// 📦 Drag and drop tools for the user interface
import draggable from 'vuedraggable'
//
// Contract arrangement automatically
import dagre from 'dagre'
// Generate a unique ID
// Deep Clone
import cloneDeep from 'lodash/cloneDeep'
//
import {
  getGraph,
  getOne,
  getEdge,
  createNode,
  updateNode,
  removeNode,
  saveGraph
} from "@/services/nodeStorageService"
// =============================
// 📍 Static Variables
// =============================
// 📌 Graph Data
const nodes = ref([])
const edges = ref([])
// 📌 Selection
const selectedNode = ref(null)
const selectedNodes = ref([])
const selectedEdge = ref([])
// 📌 Layout Flag
const isLayouting = ref(false)
// 📌 History System
const history = ref([])
const historyIndex = ref(-1)
const isRestoring = ref(false)
// VueFlow Controls
const { zoomIn, zoomOut, fitView } = useVueFlow()
/* ===================================================
📦 1️⃣ Lifecycle
=================================================== */

onMounted(initGraph)
onUnmounted(() =>
  window.removeEventListener('keydown', handleKeyPress)
)

function initGraph() {
  loadGraph()
  saveToHistory()
  window.addEventListener('keydown', handleKeyPress)
}

/* ===================================================
📖 2️⃣ LOAD GRAPH
=================================================== */

function loadGraph() {
  const graph = getGraph()
  if (graph.nodes.length) {
    nodes.value = graph.nodes
    edges.value = graph.edges
  } else {
    createDefaultGraph()
  }
}

function createDefaultGraph() {
  const startId = nanoid()
  const endId = nanoid()

  nodes.value = [
    { id: startId, position: { x: 100, y: 80 }, data: { label: "Start 🚀" } },
    { id: endId, position: { x: 300, y: 200 }, data: { label: "End 🏁" } }
  ]

  edges.value = [
    { id: nanoid(), source: startId, target: endId }
  ]
}

/* ===================================================
➕ 3️⃣ CREATE
=================================================== */

function addNode() {
  const newNode = {
    id: nanoid(),
    position: { x: 100, y: 220 },
    data: { label: "Dynamic Node 🚀" }
  }
  createNode(newNode)        // 💾 حفظ في Storage
  syncGraph()                // 🔄 تحديث Vue State
}
function syncGraph() {
  const graph = getGraph()
  nodes.value = graph.nodes
  edges.value = graph.edges
}

function duplicateNode(node) {
  nodes.value.push({
    id: nanoid(),
    position: {
      x: node.position.x + 30,
      y: node.position.y + 30
    },
    data: {
      ...node.data,
      label: node.data.label + " Copy"
    }
  })
}

function addEdge(params) {
  edges.value.push({
    ...params,
    id: nanoid()
  })
}

/* ===================================================
🔍 4️⃣ READ
=================================================== */

function getSingleNode(e) {
  const node = getOne(e.node.id)
  selectedNode.value = node
  selectedEdge.value = null
  console.log("Node From Storage:", node)
}

function getSingleEdge(e) {
  const edge = getEdge(e.edge.id)
  selectedEdge.value = edge
  selectedNode.value = null
  console.log("Edge From Storage:", edge)
}

/* ===================================================
✏️ 5️⃣ UPDATE
=================================================== */

function updateFirstNode() {
  if (!nodes.value.length) return
  updateNode(nodes.value[0].id, {
    data: { label: "Updated ✨" }
  })
  syncGraph()
}

/* ===================================================
🗑 6️⃣ DELETE
=================================================== */

function removeNodeById(id) {
  removeNode(id)   // 💾 حذف من Storage
  syncGraph()      // 🔄 تحديث Vue
}

function deleteLastNode() {
  if (!nodes.value.length) return
  removeNodeById(nodes.value[nodes.value.length - 1].id)
}

function deleteSelected() {
  const ids = selectedNodes.value.map(n => n.id)

  nodes.value = nodes.value.filter(n => !ids.includes(n.id))

  edges.value = edges.value.filter(
    e => !ids.includes(e.source) && !ids.includes(e.target)
  )

  selectedNodes.value = []
}

/* ===================================================
📐 7️⃣ AUTO LAYOUT (Dagre)
=================================================== */

function autoLayout(dir = 'TB') {
  isLayouting.value = true

  const g = new dagre.graphlib.Graph()

  g.setGraph({
    rankdir: dir,
    nodesep: 50,
    ranksep: 80
  })

  g.setDefaultEdgeLabel(() => ({}))

  nodes.value.forEach(node => {
    g.setNode(node.id, { width: 180, height: 60 })
  })

  edges.value.forEach(edge => {
    g.setEdge(edge.source, edge.target)
  })

  dagre.layout(g)

  nodes.value = nodes.value.map(node => {
    const pos = g.node(node.id)

    return {
      ...node,
      position: {
        x: pos.x - 90,
        y: pos.y - 30
      }
    }
  })

  setTimeout(() => {
    isLayouting.value = false
  }, 400)
}

/* ===================================================
🧹 8️⃣ CLEAR STORAGE
=================================================== */

function clearStorage() {
  localStorage.removeItem('vueflow_graph')
  nodes.value = []
  edges.value = []
}

/* ===================================================
↩️ 9️⃣ HISTORY SYSTEM
=================================================== */

function saveToHistory() {
  const snapshot = {
    nodes: cloneDeep(nodes.value),
    edges: cloneDeep(edges.value)
  }

  history.value = history.value.slice(0, historyIndex.value + 1)
  history.value.push(snapshot)
  historyIndex.value++
}

function undo() {
  if (historyIndex.value <= 0) return
  historyIndex.value--
  restoreState()
}

function redo() {
  if (historyIndex.value >= history.value.length - 1) return
  historyIndex.value++
  restoreState()
}

function restoreState() {
  isRestoring.value = true

  const state = history.value[historyIndex.value]

  nodes.value = cloneDeep(state.nodes)
  edges.value = cloneDeep(state.edges)

  nextTick(() => {
    isRestoring.value = false
  })
}

/* ===================================================
⌨️ 10️⃣ Keyboard Shortcuts
=================================================== */

function handleKeyPress(e) {
  if (e.key === 'Delete' && selectedNode.value) {
    removeNodeById(selectedNode.value.id)
  }

  if (e.ctrlKey && e.key === 'z') undo()
  if (e.ctrlKey && e.key === 'y') redo()
}

/* ===================================================
💾 11️⃣ Auto Save (Debounced)
=================================================== */

const debouncedSave = debounce(() => {
  saveGraph(nodes.value, edges.value)
  saveToHistory()
}, 500)

watch([nodes, edges], debouncedSave, { deep: true })
</script>

<template>
  <main class="h-screen p-4 grid grid-cols-12 gap-4 ">
    <aside class="col-span-3 border rounded p-4 overflow-auto space-y-6">
      <div class="wrapper_control">
        <div class="wrapper_control_node">
          <button type="button" @click="addNode">Add Node</button>
          <button type="button" @click="updateFirstNode">Update Node Label</button>
          <button type="button" @click="deleteLastNode"> Delete List Node</button>
          <button @click="deleteSelected">Delete Selected 🗑</button>
          <button type="button" @click="clearStorage"> clear Storage</button>
        </div>
        <div class="wrapper_control_node_data">
          <div v-if="selectedNode" class="side-panel">
            <h3>Node Settings ⚙️</h3>
            <input v-model="selectedNode.data.label" />
          </div>

          <div v-if="selectedEdge" class="side-panel">
            <h3>Edge Settings 🔗</h3>
            <p>From: {{ selectedEdge.source }}</p>
            <p>To: {{ selectedEdge.target }}</p>
          </div>
        </div>
        <div class="wrapper_control_node_layout_buttons layout-buttons flex gap-2 mb-4">
          <button @click="autoLayout('LR')">LR 📐</button>
          <button @click="autoLayout('RL')">RL 📐</button>
          <button @click="autoLayout('TB')">TB 📐</button>
          <button @click="autoLayout('BT')">BT 📐</button>
        </div>
        <div class="wrapper_control_node_side_panel side-panel">
          <h3>Nodes List ⚡</h3>
          <draggable v-model="nodes" item-key="id" animation="200">
            <template #item="{ element, index }">
              <div class="node-item" :class="{ selected: selectedNode?.id === element.id }"
                @click="selectedNode = element; selectedEdge = null">
                {{ index + 1 }}. {{ element.data.label }}
                <span @click.stop="duplicateNode(element)"> Duplicate </span>
                <span @click.stop="removeNodeById(element.id)">Delete</span>

              </div>
            </template>
          </draggable>
        </div>
      </div>
    </aside>
    <section class="col-span-9 border rounded">
      <div class="VueFlow_Component_Name">
        <!-- eslint-disable vue/no-v-model-argument -->
        <VueFlow v-model:nodes="nodes" v-model:edges="edges" :default-zoom="1.5" :min-zoom="0.2" :max-zoom="5"
          @node-click="getSingleNode" @edge-click="getSingleEdge" @connect="addEdge"
          @selection-change="onSelectionChange" :class="{ layouting: isLayouting }" :snap-to-grid="true"
          :snap-grid="[20, 20]">
          <Background pattern-color="#aaa" :gap="8" />
          <MiniMap />
          <Controls />
          <Panel position="top-right" style="display:flex; gap:5px;" class="wrapper_control_panel">
            <button @click="zoomIn()">+</button>
            <button @click="zoomOut()">-</button>
            <button @click="fitView()">Fit</button>
          </Panel>
        </VueFlow>
      </div>
    </section>
  </main>
</template>



<script>
export default { name: 'AboutView' }
</script>
