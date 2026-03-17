<!-- <script setup>
// ===================================================
// 📦 1️⃣ Imports (المكتبات المستخدمة)
// ===================================================
// 🧠 Vue Composition API
import { ref, onMounted, watch } from 'vue'
// 🔗 VueFlow (المكتبة الأساسية للرسم والـ Drag & Drop)
import { VueFlow } from '@vue-flow/core'
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
// Contract arrangement automatically
import dagre from 'dagre'

// 💾 Service مسؤول عن التخزين في LocalStorage
import {
  getGraph,
  getOne,
  getEdge,
  createNode,
  updateNode,
  removeNode,
  removeEdge,
  saveGraph,
} from '@/services/nodeStorageService'
// ===================================================
// 📍 2️⃣ State (البيانات التفاعلية)
// ===================================================
// 📦 كل الـ Nodes الموجودة في الرسم
const nodes = ref([])
// 🔗 كل الـ Edges (الروابط بين الـ Nodes)
const edges = ref([])
// 📌 Selection
const selectedNode = ref(null)
const selectedEdge = ref([])
// 📌 Layout Flag
const isLayouting = ref(false)

// ===================================================
// 🚀 3️⃣ Lifecycle (تشغيل أول ما الصفحة تفتح)
// ===================================================
// 👂 لما الكمبوننت يتركب
onMounted(initGraph)
// 🔄 تهيئة الجراف
function initGraph() {
  loadGraph()
}
// ===================================================
// 📖 4️⃣ LOAD GRAPH (تحميل البيانات)
// ===================================================
function loadGraph() {
  // 📥 نقرأ البيانات من LocalStorage
  const graph = getGraph()
  // 🧠 لو فيه بيانات محفوظة
  if (graph.nodes.length) {
    nodes.value = graph.nodes
    edges.value = graph.edges
  } else {
    // 🆕 لو مفيش بيانات → ننشئ جراف افتراضي
    createDefaultGraph()
  }
}
// ===================================================
// 🆕 5️⃣ Create Default Graph (أول تشغيل)
// ===================================================
function createDefaultGraph() {
  // 🆔 إنشاء ID فريد
  const startId = nanoid()
  const endId = nanoid()
  // 📦 إنشاء Nodes
  nodes.value = [
    {
      id: startId,
      position: { x: 100, y: 80 },
      data: { label: 'Start 🚀' },
    },
    {
      id: endId,
      position: { x: 300, y: 200 },
      data: { label: 'End 🏁' },
    },
  ]
  // 🔗 ربط Start → End
  edges.value = [
    {
      id: nanoid(),
      source: startId,
      target: endId,
    },
  ]
}
/* ===================================================
🔍 4️⃣ READ
=================================================== */

/**
 * 🧩 getSingleNode(e)
 * 🎯 وظيفتها: جلب Node واحدة من التخزين عند الضغط عليها
 * 🧠 الفكرة:
 * VueFlow بيبعت لنا Event فيه بيانات العقدة
 * لكن إحنا بنرجع نجيبها من Storage علشان يكون المصدر واحد (Source of Truth)
 */
function getSingleNode(e) {
  // 🆔 استخراج الـ ID من الحدث
  const nodeId = e.node.id

  // 📦 جلب العقدة من التخزين باستخدام Service
  const node = getOne(nodeId)

  // 🎯 تخزين العقدة المختارة لعرضها في الـ Side Panel
  selectedNode.value = node

  // ❌ إلغاء تحديد أي Edge
  selectedEdge.value = null

  // 🖥️ طباعة في الكونسول للتأكد
  console.log('📦 Node From Storage:', node)
}

/**
 * 🔗 getSingleEdge(e)
 * 🎯 وظيفتها: جلب Edge واحدة عند الضغط عليها
 * 🧠 نفس الفكرة بالظبط لكن مع الروابط
 */
function getSingleEdge(e) {
  // 🆔 استخراج ID الرابط
  const edgeId = e.edge.id

  // 📦 جلب الرابط من التخزين
  const edge = getEdge(edgeId)

  // 🎯 تخزين الرابط المختار
  selectedEdge.value = edge

  // ❌ إلغاء تحديد أي Node
  selectedNode.value = null

  // 🖥️ طباعة للتأكد
  console.log('🔗 Edge From Storage:', edge)
}

/* ===================================================
➕ 3️⃣ CREATE
=================================================== */

/**
 * ➕ addNode()
 * 🎯 وظيفتها: إنشاء Node جديدة داخل النظام
 * 🧠 الفكرة:
 * 1- ننشئ كائن يمثل العقدة
 * 2- نحفظه في الـ Storage
 * 3- نعمل Sync مع Vue علشان يحصل Re-render
 */
function addNode() {
  // 🆔 إنشاء ID فريد لكل Node
  const newNode = {
    id: nanoid(), // 🔑 ID فريد باستخدام مكتبة nanoid
    position: { x: 100, y: 220 }, // 📍 مكان الظهور على الشاشة
    data: { label: 'Dynamic Node 🚀' }, // 🏷️ البيانات الخاصة بالعقدة
  }
  // 💾 حفظ العقدة داخل Storage Service
  createNode(newNode)
  // 🔄 تحديث حالة Vue بالبيانات الجديدة
  syncGraph()
}
/**
 * 🔄 syncGraph()
 * 🎯 وظيفتها: مزامنة البيانات بين Storage و Vue State
 * 🧠 ليه بنعملها؟
 * لأننا بنخلي المصدر الأساسي للبيانات هو الـ Storage
 * وبعد أي تعديل نرجع نقرأ منه ونعكسه على Vue
 */
function syncGraph() {
  // 📦 جلب كل البيانات من التخزين
  const graph = getGraph()
  // 🧩 تحديث العقد
  nodes.value = graph.nodes
  // 🔗 تحديث الروابط
  edges.value = graph.edges
}
/**
 * 🔗 addEdge()
 * 🎯 وظيفتها: إنشاء رابط بين عقدتين
 * 🧠 params بتيجي من VueFlow event (@connect)
 */
// function addEdge(params) {
//   edges.value.push({
//     ...params,       // 📥 بيانات المصدر والهدف
//     id: nanoid()     // 🆔 إنشاء ID فريد للرابط
//   })
// }
function addEdge(params) {
  // 🚫 منع التكرار: تحقق إن مفيش edge موجودة بالفعل
  const exists = edges.value.some((e) => e.source === params.source && e.target === params.target)

  // 🛑 لو موجودة → اخرج من غير ما تضيف
  if (exists) return

  edges.value.push({
    ...params,
    id: nanoid(),
  })
}

/* ===================================================
✏️ 5️⃣ UPDATE
=================================================== */

/*
🎯 updateFirstNode()
📌 الهدف: تحديث أول Node موجود في الجراف
*/
function updateFirstNode() {
  if (!nodes.value.length) return // 🚫 لو مفيش Nodes اخرج

  updateNode(nodes.value[0].id, {
    // 🆔 نجيب أول Node
    data: { label: 'Updated ✨' }, // ✨ نعدل البيانات
  })

  syncGraph() // 🔄 نعمل مزامنة مع Vue State
}

/*
🎯 updateNodeById(id)
📌 الهدف: تحديث Node معين باستخدام الـ id
🆔 id → هو المعرف الفريد للـ Node
*/
function updateNodeById(id) {
  if (!id) return // 🚫 تأكد إن في id

  updateNode(id, {
    // 🆔 نستخدم الـ id مباشرة
    data: {
      label: selectedNode.value.data.label, // ✍️ ناخد القيمة من input
    },
  })

  syncGraph() // 🔄 تحديث الحالة بعد التعديل
}

/* ===================================================
🗑 6️⃣ DELETE
=================================================== */

function removeNodeById(id) {
  removeNode(id) // 💾 حذف من Storage
  syncGraph() // 🔄 تحديث Vue
}
function removeEdgeById(id) {
  removeEdge(id) // 💾 حذف من Storage
  syncGraph() // 🔄 تحديث Vue
}
function clearStorage() {
  localStorage.removeItem('vueflow_graph')
  nodes.value = []
  edges.value = []
}

/* ===================================================
📐 7️⃣ AUTO LAYOUT (Dagre)
=================================================== */

/*
🎯 autoLayout(dir)
📐 الهدف: ترتيب الـ Nodes تلقائيًا باستخدام Dagre
🧭 dir:
   'TB' = Top ➝ Bottom ⬇️
   'LR' = Left ➝ Right ➡️
*/
function autoLayout(dir = 'TB') {
  // 🚦 تفعيل حالة الـ Layout (لإضافة Animation مثلاً)
  isLayouting.value = true

  // 🧠 إنشاء جراف جديد في Dagre
  const g = new dagre.graphlib.Graph()

  // ⚙️ إعدادات الجراف
  g.setGraph({
    rankdir: dir, // 🧭 اتجاه الترتيب
    nodesep: 50, // ↔️ مسافة بين الـ Nodes أفقيًا
    ranksep: 80, // ↕️ مسافة بين الصفوف
  })

  // 🔗 إعداد افتراضي للـ Edges
  g.setDefaultEdgeLabel(() => ({}))

  // 🧩 إضافة الـ Nodes إلى Dagre مع أبعاد ثابتة
  nodes.value.forEach((node) => {
    g.setNode(node.id, {
      width: 180, // 📏 عرض العقدة
      height: 60, // 📐 ارتفاع العقدة
    })
  })

  // 🔗 إضافة الـ Edges إلى Dagre
  edges.value.forEach((edge) => {
    g.setEdge(edge.source, edge.target)
  })

  // 🚀 تشغيل خوارزمية الترتيب
  dagre.layout(g)

  // 🔄 تحديث مواقع الـ Nodes في VueFlow
  nodes.value = nodes.value.map((node) => {
    const pos = g.node(node.id) // 📍 الموقع الجديد من Dagre

    return {
      ...node,
      position: {
        x: pos.x - 90, // 🧮 تصحيح المنتصف (width / 2)
        y: pos.y - 30, // 🧮 تصحيح المنتصف (height / 2)
      },
    }
  })

  // ⏳ إنهاء حالة الـ Layout بعد الأنيميشن
  setTimeout(() => {
    isLayouting.value = false
  }, 400)
}
/*
🔎 findIsolatedNodes()
🎯 اكتشاف العقد المعزولة
*/
function findIsolatedNodes() {
  const connected = new Set()

  // 🧠 تجميع كل النود المتوصلة
  edges.value.forEach((e) => {
    connected.add(e.source)
    connected.add(e.target)
  })

  // 🎯 تحديد المعزولين فقط
  const isolatedIds = nodes.value.filter((n) => !connected.has(n.id)).map((n) => n.id)

  // 🚨 إضافة الكلاس
  nodes.value = nodes.value.map((n) => ({
    ...n,
    class: isolatedIds.includes(n.id) ? 'isolated-node' : '',
  }))

  // ⏳ بعد مدة → إزالة الكلاس تلقائيًا
  setTimeout(() => {
    nodes.value = nodes.value.map((n) => ({
      ...n,
      class: '',
    }))
  }, 3000) // 👈 المدة 2 ثانية (غيرها براحتك)
}
// ===================================================
// 💾 6️⃣ Auto Save (حفظ تلقائي)
// ===================================================
// ⏳ Debounce: يمنع الحفظ كل جزء من الثانية
// بدل ما يحفظ كل حركة Drag
const debouncedSave = debounce(() => {
  // 💾 احفظ الجراف بالكامل
  saveGraph(nodes.value, edges.value)
}, 500) // بعد 500ms من آخر تغيير
// 👀 مراقبة أي تغيير في nodes أو edges
watch(
  [nodes, edges], // 👈 نراقب الاتنين
  debouncedSave, // 👈 لما يحصل تغيير ننفذ الحفظ
  { deep: true }, // 👈 نراقب التغييرات الداخلية
)
</script>

<template>
  <main class="h-screen p-4 grid grid-cols-12 gap-4">
    <aside class="col-span-3 border rounded p-4 overflow-auto space-y-6">
      <h2 class="aside_title m-auto text-3xl">Controls</h2>
      <div class="wrapper_control">
        <div class="wrapper_control_node">
          <h4 class="aside_subtitle text-2xl">Node Control</h4>
          <button type="button" @click="addNode">➕ Add Node</button>
          <button type="button" @click="updateFirstNode">✏️ Update First Node Label</button>
          <button type="button" @click="clearStorage">🧹 clear Storage</button>
          <button type="button" @click="findIsolatedNodes">find Isolated Nodes</button>
        </div>
        <div class="wrapper_control_node_data">
          <div v-if="selectedNode" class="node_data">
            <h4 class="aside_subtitle text-2xl">Node Settings ⚙️</h4>

            <div class="node_update_data">
              <input v-model="selectedNode.data.label" />
              <button type="button" @click="updateNodeById(selectedNode.id)">Update</button>
              <button type="button" @click="removeNodeById(selectedNode.id)">DELETE</button>
            </div>
          </div>
          <div v-if="selectedEdge" class="edge_data">
            <h4 class="aside_subtitle text-2xl">Edge Settings 🔗</h4>
            <div class="edge_update_data">
              <p>From:{{ nodes.find((n) => n.id === selectedEdge.source)?.data.label }}</p>
              <p>To: {{ nodes.find((n) => n.id === selectedEdge.target)?.data.label }}</p>
              <button type="button" @click="removeEdgeById(selectedEdge.id)">DELETE</button>
            </div>
          </div>
        </div>
        <div class="wrapper_control_node_layout_buttons layout-buttons">
          <h4 class="aside_subtitle text-2xl">📐 Auto Layout Node</h4>
          <div class="inner_control_node_layout_buttons">
            <button @click="autoLayout('LR')">LR 📐</button>
            <button @click="autoLayout('RL')">RL 📐</button>
            <button @click="autoLayout('TB')">TB 📐</button>
            <button @click="autoLayout('BT')">BT 📐</button>
          </div>
        </div>
      </div>
    </aside>
    <section class="col-span-9 border rounded">
      <div class="VueFlow_Component_Name">
        <VueFlow
          v-model:nodes="nodes"
          v-model:edges="edges"
          :default-zoom="1.5"
          :min-zoom="0.2"
          :max-zoom="5"
          @node-click="getSingleNode"
          @edge-click="getSingleEdge"
          @connect="addEdge"
          @selection-change="onSelectionChange"
          :class="{ layouting: isLayouting }"
          :snap-to-grid="true"
          :snap-grid="[20, 20]"
        >
          <Background pattern-color="#aaa" :gap="8" />
          <MiniMap />
          <Controls />
          <Panel position="top-right" style="display: flex; gap: 5px" class="wrapper_control_panel">
            <button @click="zoomIn()">+</button>
            <button @click="zoomOut()">-</button>
            <button @click="fitView()">Fit</button>
          </Panel>
        </VueFlow>
      </div>
    </section>
  </main>
</template> -->

<style lang="scss">
// Style For Explain
main {
  section {
    .VueFlow_Component_Name {
      height: 98vh;
      overflow: hidden;
      margin: auto;
      position: relative;
    }
  }
}
</style>

<script>
export default { name: 'AboutView' }
</script>
<script setup>
// ==================================================
// 📦 Imports
// ==================================================
import { ref, onMounted, computed, watch, reactive } from 'vue'
import { VueFlow, Panel, useVueFlow } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
import { debounce } from 'lodash'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import dagre from 'dagre'

import CustomNode from '@/components/Automation/Node/CustomNode.vue'
import CustomEdge from '@/components/Automation/Edge/CustomEdge.vue'
import ActionPanel from '@/components/Automation/Action/ActionPanel.vue'
import CreateProgram from '@/components/Automation/Program/CreateProgram.vue'
import LiveConsole from '@/components/Automation/Execution/LiveConsole.vue'
import ApiFlowPanel from '@/components/ApiFlowPanel.vue'

import automationService from '@/services/AutomationService'
import { useApiTracker } from '@/composables/useApiTracker'

// ✅ الـ 4 Stores — كل store بيتولى domain معين
import { useProgramStore } from '@/stores/useProgramStore'
import { useProgramElementStore } from '@/stores/useProgramElementStore'
import { useWorkflowStore } from '@/stores/useWorkflowStore'
import { useTaskStore } from '@/stores/useTaskStore'

// ==================================================
// 🔌 Init
// ==================================================
const toast = useToast()
const confirm = useConfirm()
const { project } = useVueFlow()
const tracker = useApiTracker() // ← instance واحدة للـ ApiFlowPanel

// ✅ استدعاء الـ stores — بيرجع reactive objects
const programStore = useProgramStore()
const elementStore = useProgramElementStore()
const workflowStore = useWorkflowStore()
const taskStore = useTaskStore()

// ==================================================
// 🛠️ useAsyncAction — UX Engine
// ==================================================
// كل API call بيمر عبر tracker.execute
// → بيظهر تلقائياً في ApiFlowPanel
// ==================================================
function useAsyncAction() {
  const loading = ref(false)

  const run = async (apiFn, options = {}) => {
    if (loading.value) return // ← guard ضد double-click
    const {
      validate = null,
      successSummary = null,
      successDetail = null,
      errorSummary = 'حصل خطأ',
      onSuccess = null,
      onError = null,
    } = options

    // Validation — بيتنفذ قبل الـ API call
    if (validate) {
      const validErr = validate()
      if (validErr) {
        toast.add({
          severity: 'warn',
          summary: '⚠️ تحقق من البيانات',
          detail: validErr,
          life: 4000,
        })
        return
      }
    }

    loading.value = true
    try {
      // ✅ كل request بيمر عبر tracker → يظهر في ApiFlowPanel
      const result = await tracker.execute({ serviceFn: apiFn })

      if (successSummary)
        toast.add({
          severity: 'success',
          summary: `✅ ${successSummary}`,
          detail: successDetail,
          life: 4000,
        })

      if (onSuccess) await onSuccess(result)
      return result
    } catch (err) {
      const status = err?.response?.status
      const body = err?.response?.data
      let detail = err?.message || 'خطأ غير متوقع'

      if (status === 400 && body && typeof body === 'object') {
        detail = Object.entries(body)
          .map(([f, m]) => `${f}: ${Array.isArray(m) ? m[0] : m}`)
          .slice(0, 3)
          .join(' | ')
      } else if (status === 401) {
        detail = 'انتهت جلستك — سجّل دخول من جديد'
      } else if (status === 403) {
        detail = 'مش عندك صلاحية لهذه العملية'
      } else if (status === 404) {
        detail = 'العنصر المطلوب غير موجود'
      } else if (status === 413) {
        detail = 'الملف كبير جداً — الحد الأقصى 5MB'
      } else if (status === 500) {
        detail = 'خطأ في السيرفر — حاول مرة أخرى'
      }

      toast.add({ severity: 'error', summary: `❌ ${errorSummary}`, detail, life: 6000 })
      if (onError) onError(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return { run, loading }
}

// ← instance مستقلة لكل domain — loading states منفصلة
const programAction = useAsyncAction()
const elementAction = useAsyncAction()
const workflowAction = useAsyncAction()
const taskAction = useAsyncAction()
const nodeAction = useAsyncAction()

// ==================================================
// 🎨 UI State — خاص بالـ View فقط (مش في الـ store)
// ==================================================
const createProgramVisible = ref(false)
const editProgramVisible = ref(false)
const createProgramElementsVisible = ref(false)
const editProgramElementsVisible = ref(false)
const createTaskVisible = ref(false)
const editTaskVisible = ref(false)

const showActionPanel = ref(false)
const newActionTypeForPanel = ref('open_program')
const selectedNode = ref(null)
const draggedItem = ref(null)
const isLayoutingWorkflow = ref(false)

// Delays — state بسيط مش محتاج store
const delays = ref([])
const loadingDelays = ref(false)

// Node & Edge types للـ VueFlow
const nodeTypes = computed(() => ({ custom: CustomNode }))
const edgeTypes = computed(() => ({ custom: CustomEdge }))

// Queue للـ position sync (bypass tracker عشان مش محتاج يظهر في ApiFlowPanel)
const workflowState = reactive({ updateQueue: [], isSyncing: false })

// ==================================================
// 🍞 Toast Shorthand
// ==================================================
const showToast = (severity, summary, detail, life = 4000) => {
  const icon = { success: '✅', error: '❌', warn: '⚠️', info: 'ℹ️' }[severity] ?? ''
  toast.add({ severity, summary: `${icon} ${summary}`, detail, life })
}

// ==================================================
// ════════════════════════════════════════════════
// 1️⃣ PROGRAMS
// ════════════════════════════════════════════════
// programStore يتولى: programs[], currentProgram, form, validation, buildFormData
// الـ view مسؤوليتها فقط: dialogs + useAsyncAction
// ==================================================

// Image — helper في الـ store يتحقق من الـ size ويكتب في store.form.image
const onImageChangeProgram = (e) => {
  const err = programStore.onImageChange(e) // ← returns error string or null
  if (err) showToast('warn', 'الملف كبير', err)
}

// CREATE
const createProgram = () =>
  programAction.run(
    // ← الـ store يبني FormData ويكلم الـ service
    () => programStore.createProgram(),
    {
      // ← الـ store يتحقق من الـ form
      validate: () => programStore.validateForm(),
      successSummary: 'تم إنشاء البرنامج',
      successDetail: `"${programStore.form.name}" أُنشئ بنجاح`,
      errorSummary: 'فشل إنشاء البرنامج',
      onSuccess: () => {
        createProgramVisible.value = false // ← يغلق بس لو نجح
      },
    },
  )

// OPEN EDIT DIALOG
const openEditProgram = async (id) => {
  try {
    // ← الـ store يجيب البيانات ويملي programStore.form
    await programStore.loadProgram(id)
    editProgramVisible.value = true
  } catch (err) {
    showToast('error', 'فشل تحميل البيانات', err?.message)
  }
}

// UPDATE
const editProgram = () =>
  programAction.run(() => programStore.updateProgram(programStore.currentProgramId), {
    validate: () => programStore.validateForm(),
    successSummary: 'تم تحديث البرنامج',
    errorSummary: 'فشل تحديث البرنامج',
    onSuccess: () => {
      editProgramVisible.value = false
    },
  })

// DELETE
const confirmDeleteProgram = (program) => {
  confirm.require({
    message: `هل أنت متأكد من حذف "${program.name}"؟`,
    header: '⚠️ تأكيد الحذف',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'نعم، احذف',
    rejectLabel: 'إلغاء',
    accept: () =>
      programAction.run(() => programStore.deleteProgram(program.id), {
        successSummary: 'تم الحذف',
        successDetail: 'تم حذف البرنامج بنجاح',
        errorSummary: 'فشل الحذف',
      }),
    reject: () =>
      toast.add({ severity: 'info', summary: 'إلغاء', detail: 'لم يتم الحذف', life: 2000 }),
  })
}

// Controls — تكلم الـ store مباشرة
const openProgram = (id) =>
  programAction.run(() => programStore.openProgram(id), { errorSummary: 'فشل فتح البرنامج' })
const closeProgram = (id) =>
  programAction.run(() => programStore.closeProgram(id), { errorSummary: 'فشل إغلاق البرنامج' })
const focusProgram = (id) =>
  programAction.run(() => programStore.focusProgram(id), {
    successSummary: 'تم التركيز',
    errorSummary: 'فشل التركيز',
  })
const maximizeProgram = (id) =>
  programAction.run(() => programStore.maximizeProgram(id), {
    successSummary: 'تم التكبير',
    errorSummary: 'فشل التكبير',
  })
const statusProgram = (id) => programStore.statusProgram(id) // ← مباشر بدون loader

// ==================================================
// ════════════════════════════════════════════════
// 2️⃣ PROGRAM ELEMENTS
// ════════════════════════════════════════════════
// elementStore يتولى: elements[], currentElement, form, SELECTOR_TYPES
// ==================================================

const onImageChangeProgramElement = (e) => {
  const err = elementStore.onImageChange(e)
  if (err) showToast('warn', 'الملف كبير', err)
}

// CREATE
const createProgramElement = () =>
  elementAction.run(() => elementStore.createElement(), {
    validate: () => elementStore.validateForm(),
    successSummary: 'تم إنشاء العنصر',
    errorSummary: 'فشل إنشاء العنصر',
    onSuccess: () => {
      createProgramElementsVisible.value = false
    },
  })

// OPEN EDIT
const openEditProgramElement = async (id) => {
  try {
    await elementStore.loadElement(id) // ← يملي elementStore.form
    editProgramElementsVisible.value = true
  } catch (err) {
    showToast('error', 'فشل تحميل البيانات', err?.message)
  }
}

// UPDATE
const editProgramElement = () =>
  elementAction.run(() => elementStore.updateElement(elementStore.currentElementId), {
    validate: () => elementStore.validateForm(),
    successSummary: 'تم تحديث العنصر',
    errorSummary: 'فشل تحديث العنصر',
    onSuccess: () => {
      editProgramElementsVisible.value = false
    },
  })

// DELETE
const confirmDeleteProgramElement = (el) => {
  confirm.require({
    message: `هل تريد حذف "${el.name}"؟`,
    header: '⚠️ تأكيد الحذف',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'نعم، احذف',
    rejectLabel: 'إلغاء',
    accept: () =>
      elementAction.run(() => elementStore.deleteElement(el.id), {
        successSummary: 'تم الحذف',
        errorSummary: 'فشل الحذف',
      }),
    reject: () => toast.add({ severity: 'info', summary: 'إلغاء', life: 2000 }),
  })
}

// ==================================================
// ════════════════════════════════════════════════
// 3️⃣ WORKFLOWS
// ════════════════════════════════════════════════
// workflowStore يتولى: workflows[], nodes[], edges[], formWorkflow,
//                      loadWorkflowEvents, saveWorkflow, autoSave, autoLayout
// ==================================================

// SELECT
const selectWorkflow = async (id) => {
  workflowStore.cancelAutoSave() // ← وقّف الـ auto save القديم
  await workflowStore.selectWorkflow(id) // ← الـ store يحمل الـ nodes + edges
}

// CREATE
const createWorkflow = () =>
  workflowAction.run(
    () =>
      workflowStore.createWorkflow({
        name: workflowStore.formWorkflow.name,
        description: workflowStore.formWorkflow.description,
        status: workflowStore.formWorkflow.status,
      }),
    {
      validate: () => (!workflowStore.formWorkflow.name?.trim() ? 'الاسم مطلوب' : null),
      successSummary: 'تم إنشاء الـ Workflow',
      errorSummary: 'فشل إنشاء الـ Workflow',
    },
  )

// SAVE
const saveWorkflow = async () => {
  // ← الـ store يعمل save ويرجع الـ refreshed selectedNode
  const refreshedNode = await workflowStore.saveWorkflow({
    selectedNode: selectedNode.value,
    showActionPanel: showActionPanel.value,
  })
  // لو الـ ActionPanel مفتوح → حدّث selectedNode بعد الـ reload
  if (refreshedNode) selectedNode.value = refreshedNode
  showToast('success', 'تم الحفظ', 'Workflow saved', 12000)
}

// UPDATE STATUS
const updateStatusWorkflow = (status) =>
  workflowAction.run(
    () => workflowStore.updateWorkflow(workflowStore.currentWorkflowId, { status }),
    {
      successSummary: 'تم تحديث الحالة',
      successDetail: `Status: ${status}`,
      errorSummary: 'فشل تحديث الحالة',
    },
  )

// DELETE
const deleteWorkflow = (id) =>
  workflowAction.run(() => workflowStore.deleteWorkflow(id), {
    successSummary: 'تم الحذف',
    errorSummary: 'فشل الحذف',
  })

// CLEAR CANVAS
const clearWorkflow = () => workflowStore.clearCanvas()

// AUTO LAYOUT
const autoLayout = (dir = 'TB') => {
  isLayoutingWorkflow.value = true
  workflowStore.autoLayout(dir) // ← dagre في الـ store
  setTimeout(() => {
    isLayoutingWorkflow.value = false
  }, 400)
}

// ==================================================
// ════════════════════════════════════════════════
// 4️⃣ NODES
// ════════════════════════════════════════════════
// nodes محفوظة في workflowStore.nodes
// الـ view بتقرأ منها وتعدّل عليها مباشرة
// ==================================================

// Helper — اجيب الـ fresh node من الـ store مش الـ stale
const getFreshNode = (nodeId) =>
  workflowStore.nodes.find((n) => n.id === nodeId || n.data?.node?.backend_id === nodeId) ??
  selectedNode.value

// ON SELECT
const onNodeSelect = async ({ node }) => {
  const fresh = getFreshNode(node.id)
  selectedNode.value = fresh ?? node
  showActionPanel.value = true
  try {
    await automationService.getWorkflowNode(node.id)
  } catch (_) {}
}

// CREATE NODE (Drag & Drop)
const createNode = async (item, dropEvent) => {
  if (!workflowStore.currentWorkflowId) {
    showToast('warn', 'لا يوجد Workflow', 'اختر Workflow الأول', 9000)
    return
  }
  workflowStore.isLoading = true
  workflowStore.cancelAutoSave()

  try {
    const position = project({ x: dropEvent.clientX, y: dropEvent.clientY })
    const actionMap = { program: 'open_program', 'program-element': 'press', delay: 'wait' }
    const actionType = actionMap[item.type] || 'custom'

    // ✅ من الـ store مباشرة — مش API call زيادة
    const programData = programStore.programById(item.id)
    const nodeLabel = programData?.name ?? item.name ?? actionType

    const uiConfig = {
      ui: {
        theme: { background: '#0f172a', border: '#334155', shadow: '#334155' },
        layout: { width: 260, height: 240, rounded: true },
      },
      inputs: [
        { key: 'text', label: 'Text', type: 'string', value: '' },
        { key: 'delay', label: 'Delay (ms)', type: 'number', value: 0 },
      ],
      ai: { enabled: false, context: {}, memory: [], suggestions: [] },
    }

    // ✅ Step 1 — Create Node (يظهر في ApiFlowPanel)
    const nodeResult = await tracker.execute({
      serviceFn: () =>
        automationService.createWorkflowNode({
          workflow: workflowStore.currentWorkflowId,
          node_type: item.type,
          label: nodeLabel,
          program: item.type === 'program' ? item.id : null,
          element: item.type === 'program-element' ? item.id : null,
          position_x: position.x,
          position_y: position.y,
          config: uiConfig,
        }),
    })
    const nodeData = nodeResult.data

    // ✅ Step 2 — Create Action (يظهر في ApiFlowPanel)
    const actionResult = await tracker.execute({
      serviceFn: () =>
        automationService.createAction({
          node: nodeData.id,
          action_type: actionType,
          payload: {},
        }),
    })
    const actionResponse = actionResult.data

    // ✅ إضافة الـ node للـ canvas — نفس structure بتاعة loadWorkflowEvents
    workflowStore.nodes.push({
      id: nodeData.id,
      type: 'custom',
      position: { x: nodeData.position_x, y: nodeData.position_y },
      data: {
        label: nodeData.label,
        node: {
          backend_id: nodeData.id,
          id: nodeData.id,
          program_name: nodeData.program_name,
          element_name: nodeData.element_name,
          node_type: nodeData.node_type,
          label: nodeData.label,
          config: nodeData.config,
          program: nodeData.program,
          element: nodeData.element,
          status: 'idle',
        },
        actions: actionResponse ? [actionResponse] : [],
      },
    })
    showToast('success', 'Node Created', nodeData.label, 9000)
  } catch (err) {
    showToast('error', 'فشل إنشاء الـ Node', err?.message, 9000)
  } finally {
    workflowStore.isLoading = false
  }
}

// DELETE NODE
const deleteNodeOnWorkflow = (id) =>
  nodeAction.run(() => automationService.deleteWorkflowNode(id), {
    successSummary: 'تم الحذف',
    errorSummary: 'فشل الحذف',
    onSuccess: () => {
      workflowStore.nodes = workflowStore.nodes.filter((n) => n.id !== id)
      workflowStore.edges = workflowStore.edges.filter((e) => e.source !== id && e.target !== id)
    },
  })

// RUN NODE
const runTaskFromNode = async (nodeData) => {
  const backendId = nodeData?.backend_id
  if (!backendId) {
    toast.add({
      severity: 'error',
      summary: 'Node Error',
      detail: 'Backend ID not found',
      life: 3000,
    })
    return
  }
  await nodeAction.run(() => automationService.runWorkflowNode(backendId), {
    successSummary: 'Node Running',
    errorSummary: 'Execution Failed',
  })
}

// CREATE NODE ACTION
const createNodeAction = async ({ nodeId, action_type }) => {
  const fresh = getFreshNode(nodeId)
  const realId = fresh?.data?.node?.backend_id ?? fresh?.id
  if (!realId) {
    toast.add({ severity: 'error', summary: '❌ Node ID missing', life: 3000 })
    return
  }

  await nodeAction.run(
    () =>
      automationService.createAction({
        node: realId,
        action_type,
        payload: buildPayloadFromUI(action_type, {}),
      }),
    {
      successSummary: 'تم إنشاء الـ Action',
      successDetail: action_type,
      errorSummary: 'فشل إنشاء الـ Action',
      onSuccess: ({ data: actionResponse }) => {
        if (!actionResponse) return
        const idx = workflowStore.nodes.findIndex(
          (n) => n.id === realId || n.data?.node?.backend_id === realId,
        )
        if (idx !== -1) {
          workflowStore.nodes[idx] = {
            ...workflowStore.nodes[idx],
            data: {
              ...workflowStore.nodes[idx].data,
              actions: [...(workflowStore.nodes[idx].data.actions ?? []), actionResponse],
            },
          }
          selectedNode.value = workflowStore.nodes[idx]
        }
      },
    },
  )
}

// UPDATE NODE ACTION — Optimistic + Rollback
const updateNodeAction = async ({ nodeId, actionId, newActionType }) => {
  const payload = buildPayloadFromUI(newActionType, {})
  const idx = workflowStore.nodes.findIndex((n) => n.id === nodeId)
  const oldActions = idx !== -1 ? [...workflowStore.nodes[idx].data.actions] : []

  // ✅ Optimistic Update — UI يتحدث فوراً
  if (idx !== -1) {
    workflowStore.nodes[idx] = {
      ...workflowStore.nodes[idx],
      data: {
        ...workflowStore.nodes[idx].data,
        actions: workflowStore.nodes[idx].data.actions.map((a) =>
          a.id === actionId ? { ...a, action_type: newActionType, payload } : a,
        ),
      },
    }
    selectedNode.value = workflowStore.nodes[idx]
  }

  await nodeAction.run(
    () => automationService.updateAction(actionId, { action_type: newActionType, payload }),
    {
      successSummary: 'تم تحديث الـ Action',
      successDetail: newActionType,
      errorSummary: 'فشل تحديث الـ Action',
      onError: () => {
        // ✅ Rollback — لو الـ API fail رجّع الـ state القديم
        if (idx !== -1) {
          workflowStore.nodes[idx] = {
            ...workflowStore.nodes[idx],
            data: { ...workflowStore.nodes[idx].data, actions: oldActions },
          }
          selectedNode.value = workflowStore.nodes[idx]
        }
      },
    },
  )
}

// DELETE NODE ACTION
const deleteNodeAction = ({ nodeId, actionId }) =>
  nodeAction.run(() => automationService.deleteAction(actionId), {
    successSummary: 'تم الحذف',
    errorSummary: 'فشل الحذف',
    onSuccess: () => {
      const idx = workflowStore.nodes.findIndex((n) => n.id === nodeId)
      if (idx !== -1) {
        workflowStore.nodes[idx] = {
          ...workflowStore.nodes[idx],
          data: {
            ...workflowStore.nodes[idx].data,
            actions: workflowStore.nodes[idx].data.actions.filter((a) => a.id !== actionId),
          },
        }
        selectedNode.value = workflowStore.nodes[idx]
      }
    },
  })

// ==================================================
// 5️⃣ EDGES
// ==================================================
const onConnect = async (params) => {
  if (!workflowStore.currentWorkflowId) return
  await nodeAction.run(
    () =>
      automationService.createWorkflowEdge({
        workflow: workflowStore.currentWorkflowId,
        source_node: params.source,
        target_node: params.target,
        condition: 'success',
      }),
    {
      successSummary: 'تم ربط الـ Nodes',
      errorSummary: 'فشل إنشاء الـ Edge',
      onSuccess: ({ data }) => {
        workflowStore.edges.push({
          id: data.id,
          source: data.source_node,
          target: data.target_node,
          type: 'default',
          data: { label: data.condition },
          animated: true,
          style: { stroke: '#4CAF50', strokeWidth: 2 },
        })
      },
    },
  )
}

// ==================================================
// 6️⃣ DRAG & DROP
// ==================================================
const startDrag = (item) => {
  draggedItem.value = item
}
const onDragOver = (e) => {
  e.preventDefault()
  e.dataTransfer.dropEffect = 'move'
}
const onDrop = async (e) => {
  e.preventDefault()
  if (!draggedItem.value) return
  await createNode(draggedItem.value, e)
  draggedItem.value = null
}

// ✅ Node position — bypass tracker (مش محتاج يظهر في ApiFlowPanel)
const onNodeDragStop = ({ node }) => {
  const backendId = node.data?.node?.backend_id ?? node.id
  if (!backendId) return
  workflowState.updateQueue.push({
    type: 'node-position',
    id: backendId,
    position_x: node.position.x,
    position_y: node.position.y,
  })
  debouncedSync()
}

const processQueue = async () => {
  if (workflowState.isSyncing) return
  workflowState.isSyncing = true
  while (workflowState.updateQueue.length > 0) {
    const job = workflowState.updateQueue.shift()
    try {
      if (job.type === 'node-position')
        await automationService.updateWorkflowNode(job.id, {
          position_x: job.position_x,
          position_y: job.position_y,
        })
    } catch (err) {
      console.error('Sync error:', err)
    }
  }
  workflowState.isSyncing = false
}
const debouncedSync = debounce(processQueue, 300)

// ==================================================
// 7️⃣ ACTION HELPERS
// ==================================================
const buildPayloadFromUI = (type, extraData = {}) =>
  ({
    wait: { seconds: Number(extraData.delay || 0) },
    press: { key: extraData.key },
    hotkey: { keys: extraData.keys },
    click_element: { element_id: extraData.element_id },
    open_program: {},
  })[type] ?? {}

const handleUpdateNodeAction = ({ nodeId, newActionType, extraData }) => {
  const payload = buildPayloadFromUI(newActionType, extraData)
  workflowState.updateQueue.push({
    type: 'action',
    nodeId,
    action_type: newActionType,
    payload,
  })
  debouncedSync()
}

// ==================================================
// 8️⃣ WORKFLOW EXECUTION
// ==================================================
const startWorkflow = () =>
  workflowAction.run(() => automationService.runWorkflow(workflowStore.currentWorkflowId), {
    validate: () => (!workflowStore.currentWorkflowId ? 'اختر Workflow الأول' : null),
    successSummary: '🚀 Workflow Started',
    successDetail: 'Workflow Started successfully',
    errorSummary: 'فشل تشغيل الـ Workflow',
    onSuccess: ({ data }) => {
      // ✅ الـ taskStore يحفظ الـ run id
      taskStore.setTaskRunId(data.task_run_id)
    },
  })

// ==================================================
// ════════════════════════════════════════════════
// 9️⃣ TASKS
// ════════════════════════════════════════════════
// taskStore يتولى: tasks[], currentTask, form, validation
// ==================================================

// CREATE
const createTask = () =>
  taskAction.run(() => taskStore.createTask(), {
    validate: () => taskStore.validateForm(),
    successSummary: 'تم إنشاء الـ Task',
    errorSummary: 'فشل إنشاء الـ Task',
    onSuccess: () => {
      createTaskVisible.value = false
    },
  })

// OPEN EDIT
const openEditTask = async (id) => {
  try {
    await taskStore.loadTask(id) // ← يملي taskStore.form
    editTaskVisible.value = true
  } catch (err) {
    showToast('error', 'فشل تحميل البيانات', err?.message)
  }
}

// UPDATE
const editTask = () =>
  taskAction.run(() => taskStore.updateTask(taskStore.currentTaskId), {
    validate: () => taskStore.validateForm(),
    successSummary: 'تم تحديث الـ Task',
    errorSummary: 'فشل تحديث الـ Task',
    onSuccess: () => {
      editTaskVisible.value = false
    },
  })

// DELETE
const confirmDeleteTask = (task) => {
  confirm.require({
    message: `هل تريد حذف "${task.name}"؟`,
    header: '⚠️ تأكيد الحذف',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'نعم، احذف',
    rejectLabel: 'إلغاء',
    accept: () =>
      taskAction.run(() => taskStore.deleteTask(task.id), {
        successSummary: 'تم الحذف',
        errorSummary: 'فشل الحذف',
      }),
    reject: () => toast.add({ severity: 'info', summary: 'إلغاء', life: 2000 }),
  })
}

// ==================================================
// 💾 AutoSave — watch workflowStore.nodes + edges
// ==================================================
watch(
  // ✅ بنراقب الـ nodes والـ edges اللي في الـ store مباشرة
  [() => workflowStore.nodes, () => workflowStore.edges],
  () => {
    workflowStore.triggerAutoSave({
      selectedNode: selectedNode.value,
      showActionPanel: showActionPanel.value,
    })
  },
  { deep: true },
)

// مزامنة program مع element form
watch(
  () => programStore.currentProgramId,
  (id) => {
    if (id) elementStore.form.program = id
  },
)

// ==================================================
// 🚀 onMounted — تحميل كل البيانات في نفس الوقت
// ==================================================
onMounted(async () => {
  await Promise.all([
    programStore.loadPrograms(), // ← programStore.programs
    elementStore.loadElements(), // ← elementStore.elements
    workflowStore.loadWorkflows(), // ← workflowStore.workflows
    taskStore.loadTasks(), // ← taskStore.tasks
    // Delays — state بسيط في الـ view
    automationService
      .listDelays()
      .then((r) => {
        delays.value = r.data
      })
      .catch(() => {}),
  ])

  // ✅ الـ store جاهز
  workflowStore.isInitialized = true

  // لو فيه workflow مختار من session سابقة → حمّله
  if (workflowStore.currentWorkflowId)
    await workflowStore.loadWorkflowEvents(workflowStore.currentWorkflowId)

  console.log('🟢 APP READY')
})
</script>

<template>
  <main class="h-screen p-4">
    <div class="grid grid-cols-12 gap-4 h-full">
      <!-- ═══════════════════════════════════════════
           SIDEBAR
      ═══════════════════════════════════════════ -->
      <aside class="col-span-3 border rounded p-4 overflow-auto space-y-6">
        <!-- 🖥️ Programs — programStore.programs -->
        <div>
          <div class="flex justify-between items-center my-3">
            <h3 class="text-lg font-bold"><prime_tag value="🖥️ Programs" /></h3>
            <prime_button
              @click="createProgramVisible = true"
              style="background-color: transparent; padding: 0; border: none"
            >
              <prime_tag icon="pi pi-plus" />
            </prime_button>
          </div>
          <div class="wrapper_programs">
            <!-- ✅ programStore.isLoading -->
            <div v-if="programStore.isLoading">
              <prime_skeleton
                v-for="i in 3"
                :key="i"
                height="3rem"
                width="100%"
                class="mt-2"
                borderRadius="16px"
              />
            </div>
            <!-- ✅ programStore.programs -->
            <div
              v-else
              v-for="p in programStore.programs"
              :key="p.id"
              class="p-1 rounded cursor-grab link_aside"
              draggable="true"
              @dragstart="startDrag({ type: 'program', id: p.id })"
              @click="programStore.selectProgram(p.id)"
            >
              <prime_image alt="Image" preview>
                <template #previewicon><i class="pi pi-search"></i></template>
                <template #image><img :src="p.get_image" alt="image" /></template>
                <template #preview="slotProps">
                  <img
                    :src="p.get_image"
                    alt="preview"
                    :style="slotProps.style"
                    @click="slotProps.onClick"
                  />
                </template>
              </prime_image>
              <prime_tag :value="p.name" />
              <div>
                <prime_button
                  @click.stop="openEditProgram(p.id)"
                  style="background-color: transparent; padding: 0; border: none"
                >
                  <prime_tag icon="pi pi-file-edit" />
                </prime_button>
                <prime_button
                  @click.stop="confirmDeleteProgram(p)"
                  style="background-color: transparent; padding: 0; border: none"
                >
                  <prime_tag icon="pi pi-trash" />
                </prime_button>
              </div>
            </div>
          </div>
        </div>

        <!-- 🧩 Program Elements — elementStore.elements -->
        <div>
          <div class="flex justify-between items-center my-3">
            <h3 class="text-lg font-bold"><prime_tag value="🧩 Program Elements" /></h3>
            <prime_button
              @click="createProgramElementsVisible = true"
              style="background-color: transparent; padding: 0; border: none"
            >
              <prime_tag icon="pi pi-plus" />
            </prime_button>
          </div>
          <div class="wrapper_programs">
            <!-- ✅ elementStore.isLoading -->
            <div v-if="elementStore.isLoading">
              <prime_skeleton
                v-for="i in 3"
                :key="i"
                height="3rem"
                width="100%"
                class="mt-2"
                borderRadius="16px"
              />
            </div>
            <!-- ✅ elementStore.elements -->
            <div
              v-else
              v-for="p in elementStore.elements"
              :key="p.id"
              class="p-1 rounded cursor-grab link_aside"
              draggable="true"
              @dragstart="startDrag({ type: 'program-element', id: p.id })"
              @click="elementStore.selectElement(p.id)"
            >
              <prime_image alt="Image" preview>
                <template #previewicon><i class="pi pi-search"></i></template>
                <template #image><img :src="p.get_image" alt="image" /></template>
                <template #preview="slotProps">
                  <img
                    :src="p.get_image"
                    alt="preview"
                    :style="slotProps.style"
                    @click="slotProps.onClick"
                  />
                </template>
              </prime_image>
              <prime_tag :value="p.name" />
              <div>
                <prime_button
                  @click.stop="openEditProgramElement(p.id)"
                  style="background-color: transparent; padding: 0; border: none"
                >
                  <prime_tag icon="pi pi-file-edit" />
                </prime_button>
                <prime_button
                  @click.stop="confirmDeleteProgramElement(p)"
                  style="background-color: transparent; padding: 0; border: none"
                >
                  <prime_tag icon="pi pi-trash" />
                </prime_button>
              </div>
            </div>
          </div>
        </div>

        <!-- ⏳ Delays -->
        <div>
          <div class="flex justify-between items-center my-3">
            <h3 class="text-lg font-bold"><prime_tag value="Delays" /></h3>
          </div>
          <div class="wrapper_delays">
            <div v-if="loadingDelays">
              <prime_skeleton
                v-for="i in 3"
                :key="i"
                height="3rem"
                width="100%"
                class="mt-2"
                borderRadius="16px"
              />
            </div>
            <div
              v-else
              v-for="d in delays"
              :key="d.id"
              class="p-2 rounded cursor-grab link_aside"
              draggable="true"
              @dragstart="startDrag({ type: 'delay', id: d.id })"
            >
              <i class="pi pi-stopwatch"></i>
              <prime_tag :value="d.seconds + 's'" />
              <prime_tag value="Delay" />
            </div>
          </div>
        </div>

        <!-- 🔀 Workflows — workflowStore.workflows -->
        <div>
          <h3 class="text-lg font-bold mb-3">Workflows</h3>
          <div class="space-y-2">
            <!-- ✅ workflowStore.workflows -->
            <div
              v-for="w in workflowStore.workflows"
              :key="w.id"
              class="p-2 bg-white border rounded cursor-pointer align-content-between"
              @click="selectWorkflow(w.id)"
            >
              <span>{{ w.name }}</span>
              <span
                class="text-xs px-2 py-1 rounded"
                :class="{
                  'bg-gray-200': w.status === 'draft',
                  'bg-green-200': w.status === 'active',
                  'bg-yellow-200': w.status === 'paused',
                }"
              >
                {{ w.status }}
              </span>
            </div>
          </div>
        </div>

        <!-- 📋 Tasks — taskStore.tasks -->
        <div>
          <div class="flex justify-between items-center mb-3">
            <h3 class="text-lg font-bold"><prime_tag value="Tasks Templates" /></h3>
            <prime_button
              @click="createTaskVisible = true"
              style="background-color: transparent; padding: 0; border: none"
            >
              <prime_tag icon="pi pi-plus" />
            </prime_button>
          </div>
          <div class="wrapper_programs">
            <!-- ✅ taskStore.isLoading -->
            <div v-if="taskStore.isLoading">
              <prime_skeleton
                v-for="i in 3"
                :key="i"
                height="3rem"
                width="100%"
                class="mt-2"
                borderRadius="16px"
              />
            </div>
            <!-- ✅ taskStore.tasks -->
            <div
              v-else
              v-for="t in taskStore.tasks"
              :key="t.id"
              class="p-1 rounded cursor-grab link_aside"
              draggable="true"
              @dragstart="startDrag({ type: 'task', id: t.id })"
              @click="taskStore.selectTask(t.id)"
            >
              <prime_tag :value="t.name" />
              <div>
                <prime_button
                  @click.stop="openEditTask(t.id)"
                  style="background-color: transparent; padding: 0; border: none"
                >
                  <prime_tag icon="pi pi-file-edit" />
                </prime_button>
                <prime_button
                  @click.stop="confirmDeleteTask(t)"
                  style="background-color: transparent; padding: 0; border: none"
                >
                  <prime_tag icon="pi pi-trash" />
                </prime_button>
              </div>
            </div>
          </div>
        </div>
      </aside>

      <!-- ═══════════════════════════════════════════
           CANVAS SECTION
      ═══════════════════════════════════════════ -->
      <section class="col-span-9 mb-16">
        <!-- Workflow Form — workflowStore.formWorkflow -->
        <div class="wrapper_name_description">
          <div class="inner_name_description">
            <div>
              <label class="block font-semibold mb-1">Name</label>
              <!-- ✅ workflowStore.formWorkflow.name -->
              <input
                v-model="workflowStore.formWorkflow.name"
                type="text"
                class="input"
                placeholder="Workflow name"
              />
            </div>
            <div>
              <label class="block font-semibold mb-1">Description</label>
              <!-- ✅ workflowStore.formWorkflow.description -->
              <textarea
                v-model="workflowStore.formWorkflow.description"
                class="textarea"
                cols="30"
                rows="1"
              ></textarea>
            </div>
            <div>
              <label class="block font-semibold mb-1">Status</label>
              <!-- ✅ workflowStore.formWorkflow.status -->
              <select v-model="workflowStore.formWorkflow.status" class="input">
                <option value="draft">📝 Draft</option>
                <option value="active">✅ Active</option>
                <option value="paused">⏸ Paused</option>
              </select>
            </div>
            <div>
              <!-- ✅ workflowStore.currentWorkflowId -->
              <prime_button
                label="🗑️"
                @click="deleteWorkflow(workflowStore.currentWorkflowId)"
                class="class_name"
              />
            </div>
          </div>
        </div>

        <!-- ✅ VueFlow — workflowStore.nodes + workflowStore.edges -->
        <VueFlow
          class="border rounded"
          v-model:nodes="workflowStore.nodes"
          v-model:edges="workflowStore.edges"
          :node-types="nodeTypes"
          :edge-types="edgeTypes"
          @node-click="onNodeSelect"
          @dragover="onDragOver"
          @drop="onDrop"
          @connect="onConnect"
          @nodeDragStop="onNodeDragStop"
          :pan-on-drag="[1]"
          :pan-on-scroll="true"
          :zoom-on-scroll="false"
        >
          <Background variant="dots" pattern-color="#aaa" :gap="10" />
          <Controls />
          <MiniMap />

          <template #node-custom="props">
            <CustomNode
              v-bind="props"
              @run-task="runTaskFromNode"
              @open-program="openProgram"
              @close-program="closeProgram"
              @status-program="statusProgram"
              @delete-node="deleteNodeOnWorkflow"
              @update-node-action="handleUpdateNodeAction"
            />
          </template>
          <template #edge-custom="props">
            <CustomEdge v-bind="props" />
          </template>

          <Panel position="top-left">
            <div class="flex gap-2">
              <button @click="createWorkflow" class="btn-white">➕ إنشاء Workflow جديد</button>
              <button @click="saveWorkflow" class="btn-white">💾 Save Workflow</button>
              <button @click="clearWorkflow" class="btn-white">🗑️ مسح الكل</button>
              <button @click="updateStatusWorkflow('active')">▶ Activate</button>
              <button @click="updateStatusWorkflow('paused')">⏸ Pause</button>
              <prime_button
                label="Start Workflow"
                icon="pi pi-play"
                class="p-button-success"
                :disabled="!workflowStore.currentWorkflowId"
                @click.once="startWorkflow"
              />
            </div>
            <div class="inner_control_node_layout_buttons">
              <button @click="autoLayout('LR')">LR 📐</button>
              <button @click="autoLayout('RL')">RL 📐</button>
              <button @click="autoLayout('TB')">TB 📐</button>
              <button @click="autoLayout('BT')">BT 📐</button>
            </div>
          </Panel>
        </VueFlow>
      </section>
    </div>

    <!-- ════════════════════════════════════════════
         Global Components
    ════════════════════════════════════════════ -->

    <!-- ✅ taskStore.currentTaskRunId -->
    <LiveConsole v-if="taskStore.currentTaskRunId" :taskRunId="taskStore.currentTaskRunId" />

    <!-- ✅ tracker.stages/meta/error — instance واحدة بتتحدث مع كل API call -->
    <ApiFlowPanel
      :stages="tracker.stages"
      :meta="tracker.meta"
      :error="tracker.error"
      :show-data="true"
    />

    <ActionPanel
      :show="showActionPanel"
      :selected-node="selectedNode"
      v-model:new-action-type-for-panel="newActionTypeForPanel"
      @close="showActionPanel = false"
      @create-action="createNodeAction"
      @update-action="updateNodeAction"
      @delete-action="deleteNodeAction"
    />

    <!-- ✅ programStore.form — مش formProgram محلي -->
    <CreateProgram
      v-model:visible="createProgramVisible"
      :form="programStore.form"
      @image-change="onImageChangeProgram"
      @submit="createProgram"
    />

    <!-- ═══ Edit Program Dialog ═══ -->
    <div class="card flex justify-center">
      <prime_dialog
        v-model:visible="editProgramVisible"
        pt:root:class="!border-0 !bg-transparent"
        pt:mask:class="backdrop-blur-sm"
      >
        <template #container="{ closeCallback }">
          <div
            class="flex flex-col px-8 py-8 gap-6 rounded-2xl"
            style="
              background-image: radial-gradient(
                circle at left top,
                var(--p-primary-400),
                var(--p-primary-700)
              );
            "
          >
            <div style="margin: auto; font-size: 2rem; font-weight: bolder">Edit Program</div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Program Name</label>
                <!-- ✅ programStore.form.name -->
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="programStore.form.name"
                  placeholder="Program name"
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Description</label>
                <prime_textarea
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="programStore.form.description"
                  placeholder="Program description"
                />
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Executable Path</label>
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="programStore.form.executable_path"
                  placeholder="C:/Program Files/VSCode/Code.exe"
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Project Path</label>
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="programStore.form.project_path"
                  placeholder="C:/Users/..."
                />
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Working Directory</label>
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="programStore.form.working_directory"
                  placeholder="C:/Users/..."
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Window Title Pattern</label>
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="programStore.form.window_title_pattern"
                  placeholder="Project Name"
                />
              </div>
            </div>
            <input type="file" accept="image/*" @change="onImageChangeProgram" />
            <div class="flex items-center gap-4">
              <prime_button
                label="Cancel"
                @click="closeCallback"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
              <prime_button
                label="Update"
                @click="editProgram"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
            </div>
          </div>
        </template>
      </prime_dialog>
    </div>

    <!-- ═══ Create Program Element Dialog ═══ -->
    <div class="card flex justify-center" style="overflow-y: auto">
      <prime_dialog
        v-model:visible="createProgramElementsVisible"
        pt:root:class="!border-0 !bg-transparent"
        pt:mask:class="backdrop-blur-sm"
      >
        <template #container="{ closeCallback }">
          <div
            class="flex flex-col px-8 py-8 gap-6 rounded-2xl"
            style="
              background-image: radial-gradient(
                circle at left top,
                var(--p-primary-400),
                var(--p-primary-700)
              );
            "
          >
            <div style="margin: auto; font-size: 2rem; font-weight: bolder">
              Create Program Element
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Name</label>
                <!-- ✅ elementStore.form.name -->
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="elementStore.form.name"
                  placeholder="Element name"
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Description</label>
                <prime_textarea
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="elementStore.form.description"
                  placeholder="Description"
                />
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Image</label>
                <input type="file" accept="image/*" @change="onImageChangeProgramElement" />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Program</label>
                <!-- ✅ programStore.programs في الـ select -->
                <select v-model="elementStore.form.program" class="input">
                  <option disabled value="">اختر البرنامج</option>
                  <option v-for="p in programStore.programs" :key="p.id" :value="p.id">
                    {{ p.name }}
                  </option>
                </select>
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Selector Type</label>
                <!-- ✅ elementStore.SELECTOR_TYPES -->
                <select v-model="elementStore.form.selector_type">
                  <option disabled value="">Choose selector type</option>
                  <option
                    v-for="type in elementStore.SELECTOR_TYPES"
                    :key="type.value"
                    :value="type.value"
                  >
                    {{ type.label }}
                  </option>
                </select>
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">X</label>
                <prime_input_number v-model="elementStore.form.x" inputId="integeronly" fluid />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Y</label>
                <prime_input_number v-model="elementStore.form.y" inputId="integeronly" fluid />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Width</label>
                <prime_input_number v-model="elementStore.form.width" inputId="integeronly" fluid />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Height</label>
                <prime_input_number
                  v-model="elementStore.form.height"
                  inputId="integeronly"
                  fluid
                />
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Shortcut</label>
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="elementStore.form.shortcut"
                  placeholder="Ctrl+C"
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Confidence</label>
                <prime_input_number
                  v-model="elementStore.form.confidence"
                  inputId="integeronly"
                  fluid
                />
              </div>
            </div>
            <div class="flex items-center gap-4">
              <prime_button
                label="Cancel"
                @click="closeCallback"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
              <prime_button
                label="Create"
                @click="createProgramElement"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
            </div>
          </div>
        </template>
      </prime_dialog>
    </div>

    <!-- ═══ Edit Program Element Dialog ═══ -->
    <div class="card flex justify-center">
      <prime_dialog
        v-model:visible="editProgramElementsVisible"
        pt:root:class="!border-0 !bg-transparent"
        pt:mask:class="backdrop-blur-sm"
      >
        <template #container="{ closeCallback }">
          <div
            class="flex flex-col px-8 py-8 gap-6 rounded-2xl"
            style="
              background-image: radial-gradient(
                circle at left top,
                var(--p-primary-400),
                var(--p-primary-700)
              );
            "
          >
            <div style="margin: auto; font-size: 2rem; font-weight: bolder">
              Edit Program Element
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Name</label>
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="elementStore.form.name"
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Description</label>
                <prime_textarea
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="elementStore.form.description"
                />
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Image</label>
                <input type="file" accept="image/*" @change="onImageChangeProgramElement" />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Program</label>
                <select v-model="elementStore.form.program" class="input">
                  <option disabled value="">اختر البرنامج</option>
                  <option v-for="p in programStore.programs" :key="p.id" :value="p.id">
                    {{ p.name }}
                  </option>
                </select>
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Selector Type</label>
                <select v-model="elementStore.form.selector_type">
                  <option disabled value="">Choose selector type</option>
                  <option
                    v-for="type in elementStore.SELECTOR_TYPES"
                    :key="type.value"
                    :value="type.value"
                  >
                    {{ type.label }}
                  </option>
                </select>
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">X</label>
                <prime_input_number v-model="elementStore.form.x" fluid />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Y</label>
                <prime_input_number v-model="elementStore.form.y" fluid />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Width</label>
                <prime_input_number v-model="elementStore.form.width" fluid />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Height</label
                ><prime_input_number v-model="elementStore.form.height" fluid />
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Shortcut</label>
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="elementStore.form.shortcut"
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Confidence</label>
                <prime_input_number v-model="elementStore.form.confidence" fluid />
              </div>
            </div>
            <div class="flex items-center gap-4">
              <prime_button
                label="Cancel"
                @click="closeCallback"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
              <prime_button
                label="Update"
                @click="editProgramElement"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
            </div>
          </div>
        </template>
      </prime_dialog>
    </div>

    <!-- ═══ Create Task Dialog ═══ -->
    <div class="card flex justify-center" style="overflow-y: auto">
      <prime_dialog
        v-model:visible="createTaskVisible"
        pt:root:class="!border-0 !bg-transparent"
        pt:mask:class="backdrop-blur-sm"
      >
        <template #container="{ closeCallback }">
          <div
            class="flex flex-col px-8 py-8 gap-6 rounded-2xl"
            style="
              background-image: radial-gradient(
                circle at left top,
                var(--p-primary-400),
                var(--p-primary-700)
              );
            "
          >
            <div style="margin: auto; font-size: 2rem; font-weight: bolder">Create Task</div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Task Name</label>
                <!-- ✅ taskStore.form.name -->
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="taskStore.form.name"
                  placeholder="Task Name"
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Description</label>
                <prime_textarea
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="taskStore.form.description"
                  placeholder="Task description"
                />
              </div>
            </div>
            <div class="inline-flex flex-col gap-2">
              <label class="text-primary-50 font-semibold">Program</label>
              <!-- ✅ programStore.programs في task dialog -->
              <select v-model="taskStore.form.program" class="input">
                <option disabled value="">اختر البرنامج</option>
                <option v-for="p in programStore.programs" :key="p.id" :value="p.id">
                  {{ p.name }}
                </option>
              </select>
            </div>
            <div class="flex items-center gap-4">
              <prime_button
                label="Cancel"
                @click="closeCallback"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
              <prime_button
                label="Create"
                @click="createTask"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
            </div>
          </div>
        </template>
      </prime_dialog>
    </div>

    <!-- ═══ Edit Task Dialog ═══ -->
    <div class="card flex justify-center">
      <prime_dialog
        v-model:visible="editTaskVisible"
        pt:root:class="!border-0 !bg-transparent"
        pt:mask:class="backdrop-blur-sm"
      >
        <template #container="{ closeCallback }">
          <div
            class="flex flex-col px-8 py-8 gap-6 rounded-2xl"
            style="
              background-image: radial-gradient(
                circle at left top,
                var(--p-primary-400),
                var(--p-primary-700)
              );
            "
          >
            <div style="margin: auto; font-size: 2rem; font-weight: bolder">Edit Task</div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Task Name</label>
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="taskStore.form.name"
                  placeholder="Task Name"
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Description</label>
                <prime_textarea
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="taskStore.form.description"
                  placeholder="Task description"
                />
              </div>
            </div>
            <div class="inline-flex flex-col gap-2">
              <label class="text-primary-50 font-semibold">Program</label>
              <select v-model="taskStore.form.program" class="input">
                <option disabled value="">اختر البرنامج</option>
                <option v-for="p in programStore.programs" :key="p.id" :value="p.id">
                  {{ p.name }}
                </option>
              </select>
            </div>
            <div class="flex items-center gap-4">
              <prime_button
                label="Cancel"
                @click="closeCallback"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
              <prime_button
                label="Update"
                @click="editTask"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
            </div>
          </div>
        </template>
      </prime_dialog>
    </div>
  </main>
</template>
<!-- eslint-disable vue/no-v-model-argument -->

<!--

- محتاج اول حاجة انو انا اشغال ال ApiFlowPanel.vue فى كل الفانكشان اللى  تشتغل م ال api
- انشاء Workflow Store
- محتاج الى ان أجمع  بين n8n Node-RED Zapier و CRUD Dashboard
- الكود بدل: try catch في كل مكان يصبح: asyncAction.User()

- Drag-Drop Node Marketplace
- Node Plugin System
- Node Visual Builder مثل n8n
- Node Marketplace Plugins
- AI Automation Nodes
- Plugin SDK للمطورين مثال Plugin لتشغيل برنامج
- إدارة جميع Nodes

- Workflow Database Schema احترافي
- Workflow Visual Node Builder مثل n8n بالكامل
- Workflow Templates Marketplace
- Versioning للـ workflows

- 🏗️ الهيكل الجديد للمشروع
- استخدام: shallowRef
- Background Worker (مهم جداً) لكي لا يتجمد السيرفر. استخدم: Celery
- Distributed Worker System
- Realtime Execution Graph
- Multi-tenant SaaS Architecture
-


-->

<!--
<script setup>
// ==================================================
// 📦 1️⃣ Imports
// ==================================================
import { ref, onMounted, computed, watch, reactive, shallowRef } from 'vue'
import automationService from '@/services/AutomationService'
import { VueFlow, Panel, useVueFlow } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
import vuedraggable from 'vuedraggable'
import CustomNode from '@/components/Automation/CustomNode.vue'
import CustomEdge from '@/components/Automation/CustomEdge.vue'
import ActionPanel from '@/components/Automation/ActionPanel.vue'
import CreateProgram from '@/components/Automation/Program/CreateProgram.vue'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import LiveConsole from '@/components/Automation/LiveConsole.vue'
import { debounce } from 'lodash'
import dagre from 'dagre'
import { useApiTracker } from '@/composables/useApiTracker'
// ✅ FIX 1: Wrong path was '@/composables/ApiFlowPanel.vue'
import ApiFlowPanel from '@/composables/ApiFlowPanel.vue'

const toast = useToast()
const confirm = useConfirm()
const { project } = useVueFlow()
// ==================================================

// 🛠️ INLINE UX ENGINE — useAsyncAction
// ==================================================
// Replaces all try/catch/finally blocks with a single pattern.
//
// FIXES APPLIED:
//  ❌ Before: success toast fired in `finally` → fires even on errors
//  ✅ After:  success only in `try` via onSuccess callback
//
//  ❌ Before: dialogs closed in `finally` → closes even on errors
//  ✅ After:  dialogs close only inside onSuccess
//
//  ❌ Before: no guard against double-clicking submit
//  ✅ After:  `if (loading.value) return` prevents duplicate submissions
//
//  ❌ Before: generic error.message shown to user (useless)
//  ✅ After:  reads Django 400 validation errors field-by-field
// ==================================================
function useAsyncAction() {
  const loading = ref(false)

  const run = async (asyncFn, options = {}) => {
    // ✅ Duplicate submission guard
    if (loading.value) return

    const {
      successSummary = null,
      successDetail = null,
      errorSummary = 'حصل خطأ',
      onSuccess = null,
      onError = null,
      onFinally = null,
    } = options

    loading.value = true
    try {
      const data = await asyncFn()

      // ✅ SUCCESS: toast fires ONLY here (not in finally)
      if (successSummary) {
        toast.add({
          severity: 'success',
          summary: `✅ ${successSummary}`,
          detail: successDetail,
          life: 4000,
        })
      }
      if (onSuccess) await onSuccess(data)
      return data
    } catch (err) {
      // ✅ Smart error: reads Django validation errors automatically
      const status = err?.response?.status
      const body = err?.response?.data
      let detail = err?.message || 'خطأ غير متوقع'

      if (status === 400 && body && typeof body === 'object') {
        detail = Object.entries(body)
          .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs[0] : msgs}`)
          .slice(0, 3)
          .join(' | ')
      } else if (status === 401) {
        detail = 'انتهت جلستك — سجّل دخول من جديد'
      } else if (status === 403) {
        detail = 'مش عندك صلاحية لهذه العملية'
      } else if (status === 404) {
        detail = 'العنصر المطلوب غير موجود'
      } else if (status === 413) {
        detail = 'الملف كبير جداً — الحد الأقصى 5MB'
      } else if (status === 500) {
        detail = 'خطأ في السيرفر — حاول مرة أخرى'
      }

      toast.add({ severity: 'error', summary: `❌ ${errorSummary}`, detail, life: 6000 })
      if (onError) onError(err)
      throw err
    } finally {
      loading.value = false
      if (onFinally) onFinally()
    }
  }

  return { run, loading }
}

// One async runner per domain → independent loading states
const programAction = useAsyncAction()
const programElementAction = useAsyncAction()
const workflowAction = useAsyncAction()
const taskAction = useAsyncAction()

// API Tracker
const { execute, stages, result, error: trackerError, meta } = useApiTracker()
console.log('result: ', result)

// ==================================================
// 🍞 Toast shorthand
// ==================================================
const showToast = (severity, summary, detail, life = 4000) =>
  toast.add({
    severity,
    summary: `${severity === 'success' ? '✅' : severity === 'error' ? '❌' : '⚠️'} ${summary}`,
    detail,
    life,
  })

// ==================================================
// ✅ Form Validators
// ==================================================
const validateProgram = (form) => {
  if (!form.name?.trim()) return 'اسم البرنامج مطلوب'
  if (!form.executable_path?.trim()) return 'مسار التنفيذ مطلوب'
  return null
}
const validateProgramElement = (form) => {
  if (!form.name?.trim()) return 'الاسم مطلوب'
  if (!form.program) return 'لازم تختار برنامج'
  if (!form.selector_type) return 'لازم تختار Selector Type'
  return null
}
const validateTask = (form) => {
  if (!form.name?.trim()) return 'اسم الـ Task مطلوب'
  if (!form.program) return 'لازم تختار برنامج'
  return null
}
// ✅ FIX: validate image size before upload (prevents 413 errors)
const validateImageSize = (file, maxMB = 5) => {
  if (file && file.size > maxMB * 1024 * 1024) {
    showToast('warn', 'الملف كبير', `الحد الأقصى ${maxMB}MB`)
    return false
  }
  return true
}

// ==============================================
// =================== State ===================
// ==============================================
// 1️⃣ Programs
const programs = ref([])
const loadingPrograms = ref(false)
const currentProgramId = ref(null)
const ceateProgramVisible = ref(false)
const editProgramVisible = ref(false)
const formProgram = ref({
  name: '',
  description: '',
  executable_path: '',
  project_path: '',
  working_directory: '',
  window_title_pattern: '',
  image: null,
})
const data = await execute({
  url: '/api/automation/programs/',
  method: 'POST',
  data: formProgram,
})
console.log('data: ', data)

// 2️⃣ Program Elements
const programsElement = ref([])
const loadingProgramElements = ref(false)
const currentProgramElementId = ref(null)
const ceateProgramElementsVisible = ref(false)
const editProgramElementsVisible = ref(false)
const programElementselectorTypes = [
  { label: 'Image Recognition', value: 'image' },
  { label: 'Screen Coordinates', value: 'coords' },
  { label: 'Text OCR', value: 'text' },
  { label: 'UI Automation', value: 'ui' },
]
const formProgramElement = ref({
  name: '',
  description: '',
  executable_path: '',
  project_path: '',
  working_directory: '',
  window_title_pattern: '',
  image: null,
  program: null,
  element_type: 'button',
  selector_type: null,
  selector_value: 'xpath',
  x: 0,
  y: 0,
  width: 0,
  height: 0,
  shortcut: '',
  confidence: 0,
})

// 3️⃣ Workflows
const workflows = ref([])
const loadingWorkflows = ref(false)
const isLoadingWorkflow = ref(false)
const isInitialized = ref(false)
const isLayoutingWorkflow = ref(false)
const currentWorkflowId = ref(null)
const isSavingWorkflow = ref(false)
const formWorkflow = ref({ name: '', description: '', status: 'draft' })
const workflowState = reactive({
  nodesMap: new Map(),
  edgesMap: new Map(),
  updateQueue: [],
  isSyncing: false,
})

// 4️⃣ Nodes
const nodes = shallowRef([])
const selectedNode = ref(null)
const currentNodeId = ref(null)
const nodeTypes = computed(() => ({ custom: CustomNode }))
const draggedItem = ref(null)

// 5️⃣ Edges
const edges = shallowRef([])
const edgeTypes = computed(() => ({ custom: CustomEdge }))

// 6️⃣ Actions
const showActionPanel = ref(false)
const newActionTypeForPanel = ref('open_program')

// 7️⃣ Tasks
const tasks = ref([])
const loadingTasks = ref(false)
const currentTaskId = ref(null)
const taskRunId = ref(null)
const currentTaskRunId = ref(null)
const createTaskVisible = ref(false)
const editTaskVisible = ref(false)
const formTask = ref({ name: '', description: '', program: null })

// 🔟 Delays
const delays = ref([])
const loadingDelays = ref(false)

// ==============================================
// ================ 1️⃣ PROGRAMS ================
// ==============================================

// GET ALL
const loadPrograms = async () => {
  loadingPrograms.value = true
  try {
    const { data } = await automationService.listPrograms()
    programs.value = data
  } catch (err) {
    showToast('error', 'فشل تحميل البرامج', err?.message)
  } finally {
    loadingPrograms.value = false
  }
}

// GET SINGLE
const selectProgram = async (id) => {
  if (!id) return
  currentProgramId.value = id
  await loadProgram(id)
}
const loadProgram = async (id) => {
  const { data } = await automationService.getProgram(id)
  currentProgramId.value = data.id
  formProgram.value = {
    name: data.name,
    description: data.description,
    executable_path: data.executable_path,
    project_path: data.project_path,
    working_directory: data.working_directory,
    window_title_pattern: data.window_title_pattern,
    image: null,
  }
  return data
}

// Image handlers with size validation
const onImageChangeProgram = (e) => {
  const file = e.target.files[0]
  if (!file || !validateImageSize(file)) {
    e.target.value = ''
    return
  }
  formProgram.value.image = file
}
const onImageChangeProgramElement = (e) => {
  const file = e.target.files[0]
  if (!file || !validateImageSize(file)) {
    e.target.value = ''
    return
  }
  formProgramElement.value.image = file
}

// FormData builder (extracted — no repetition)
const buildProgramFormData = (form) => {
  const fd = new FormData()
  fd.append('name', form.name)
  fd.append('description', form.description)
  fd.append('executable_path', form.executable_path)
  fd.append('project_path', form.project_path || '')
  fd.append('working_directory', form.working_directory || '')
  fd.append('window_title_pattern', form.window_title_pattern || '')
  if (form.image instanceof File) fd.append('image', form.image)
  return fd
}

// CREATE
// ✅ FIX 2: validation before API, success toast only on success, dialog closes only on success
const createProgram = () =>
  programAction.run(
    () => {
      const err = validateProgram(formProgram.value)
      if (err) {
        showToast('warn', 'تحقق من البيانات', err)
        throw new Error(err)
      }
      return automationService.createProgram(buildProgramFormData(formProgram.value))
    },
    {
      successSummary: 'تم إنشاء البرنامج',
      successDetail: `"${formProgram.value.name}" أُنشئ بنجاح`,
      errorSummary: 'فشل إنشاء البرنامج',
      onSuccess: async ({ data }) => {
        programs.value.unshift(data) // optimistic update — no full reload
        currentProgramId.value = data.id
        ceateProgramVisible.value = false // ✅ closes ONLY on success
      },
      // No onError → dialog stays open so user can fix input
    },
  )

// OPEN EDIT
const openEditProgram = async (id) => {
  if (!id) return
  try {
    currentProgramId.value = id
    await loadProgram(id)
    editProgramVisible.value = true
  } catch (err) {
    showToast('error', 'فشل تحميل البيانات', err?.message)
  }
}

// EDIT
const editProgram = () =>
  programAction.run(
    () => {
      const err = validateProgram(formProgram.value)
      if (err) {
        showToast('warn', 'تحقق من البيانات', err)
        throw new Error(err)
      }
      return automationService.updateProgram(
        currentProgramId.value,
        buildProgramFormData(formProgram.value),
      )
    },
    {
      successSummary: 'تم تحديث البرنامج',
      errorSummary: 'فشل تحديث البرنامج',
      onSuccess: async ({ data }) => {
        const idx = programs.value.findIndex((p) => p.id === data.id)
        if (idx !== -1) programs.value[idx] = { ...programs.value[idx], ...data }
        editProgramVisible.value = false // ✅ closes ONLY on success
      },
    },
  )

// DELETE
const confirmDeleteProgram = (program) => {
  confirm.require({
    message: `هل أنت متأكد من حذف "${program.name}"؟`,
    header: '⚠️ تأكيد الحذف',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'نعم، احذف',
    rejectLabel: 'إلغاء',
    accept: () => deleteProgram(program.id),
    reject: () =>
      toast.add({ severity: 'info', summary: 'إلغاء', detail: 'لم يتم الحذف', life: 2000 }),
  })
}
const deleteProgram = (id) =>
  programAction.run(() => automationService.deleteProgram(id), {
    successSummary: 'تم الحذف',
    successDetail: 'تم حذف البرنامج بنجاح',
    errorSummary: 'فشل الحذف',
    onSuccess: () => {
      programs.value = programs.value.filter((p) => p.id !== id)
      if (currentProgramId.value === id) {
        currentProgramId.value = null
        formProgram.value = {}
      }
    },
  })

// PROGRAM ACTIONS
const openProgram = (id) => automationService.openProgram(id)
const closeProgram = (id) => automationService.closeProgram(id)
const statusProgram = (id) => automationService.statusProgram(id).then((r) => r.data)
const focusProgram = (id) =>
  programAction.run(() => automationService.focusProgram(id), {
    successSummary: 'تم التركيز',
    errorSummary: 'فشل التركيز',
  })
const maximizeProgram = (id) =>
  programAction.run(() => automationService.maximizeProgram(id), {
    successSummary: 'تم التكبير',
    errorSummary: 'فشل التكبير',
  })

// ==============================================
// ============= 2️⃣ Program Elements ===========
// ==============================================

const loadProgramElements = async () => {
  loadingProgramElements.value = true
  try {
    const { data } = await automationService.listProgramElements()
    programsElement.value = data
  } catch (err) {
    showToast('error', 'فشل تحميل العناصر', err?.message)
  } finally {
    loadingProgramElements.value = false
  }
}

const selectProgramElement = async (id) => {
  if (!id) return
  currentProgramElementId.value = id
  await loadProgramElement(id)
}
const loadProgramElement = async (id) => {
  const { data } = await automationService.getProgramElement(id)
  currentProgramElementId.value = data.id
  formProgramElement.value = {
    name: data.name,
    description: data.description,
    program: data.program,
    element_type: data.element_type,
    selector_type: data.selector_type,
    selector_value: data.selector_value,
    x: data.x,
    y: data.y,
    width: data.width,
    height: data.height,
    shortcut: data.shortcut,
    confidence: data.confidence,
    image: null,
  }
  return data
}

const buildElementFormData = (form) => {
  const fd = new FormData()
  fd.append('name', form.name)
  fd.append('description', form.description)
  fd.append('program', form.program)
  fd.append('element_type', form.element_type)
  fd.append('selector_type', form.selector_type)
  fd.append('selector_value', form.selector_value)
  fd.append('x', Number(form.x))
  fd.append('y', Number(form.y))
  fd.append('width', Number(form.width))
  fd.append('height', Number(form.height))
  fd.append('shortcut', form.shortcut)
  fd.append('confidence', parseFloat(form.confidence))
  if (form.image instanceof File) fd.append('image', form.image)
  return fd
}

// CREATE Element — same pattern
const createProgramElement = () =>
  programElementAction.run(
    () => {
      const err = validateProgramElement(formProgramElement.value)
      if (err) {
        showToast('warn', 'تحقق من البيانات', err)
        throw new Error(err)
      }
      return automationService.createProgramElement(buildElementFormData(formProgramElement.value))
    },
    {
      successSummary: 'تم إنشاء العنصر',
      errorSummary: 'فشل إنشاء العنصر',
      onSuccess: async ({ data }) => {
        programsElement.value.unshift(data)
        ceateProgramElementsVisible.value = false // ✅ closes ONLY on success
        await loadProgramElements()
      },
    },
  )

const openEditProgramElement = async (id) => {
  if (!id) return
  try {
    currentProgramElementId.value = id
    await loadProgramElement(id)
    editProgramElementsVisible.value = true
  } catch (err) {
    showToast('error', 'فشل تحميل البيانات', err?.message)
  }
}

const editProgramElement = () =>
  programElementAction.run(
    () => {
      const err = validateProgramElement(formProgramElement.value)
      if (err) {
        showToast('warn', 'تحقق من البيانات', err)
        throw new Error(err)
      }
      return automationService.updateProgramElement(
        currentProgramElementId.value,
        buildElementFormData(formProgramElement.value),
      )
    },
    {
      successSummary: 'تم تحديث العنصر',
      errorSummary: 'فشل تحديث العنصر',
      onSuccess: async ({ data }) => {
        const idx = programsElement.value.findIndex((e) => e.id === data.id)
        if (idx !== -1) programsElement.value[idx] = { ...programsElement.value[idx], ...data }
        editProgramElementsVisible.value = false // ✅ closes ONLY on success
      },
    },
  )

const confirmDeleteProgramElement = (element) => {
  confirm.require({
    message: `هل أنت متأكد من حذف "${element.name}"؟`,
    header: '⚠️ تأكيد الحذف',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'نعم، احذف',
    rejectLabel: 'إلغاء',
    accept: () => deleteProgramElement(element.id),
  })
}
const deleteProgramElement = (id) =>
  programElementAction.run(() => automationService.deleteProgramElement(id), {
    successSummary: 'تم الحذف',
    errorSummary: 'فشل الحذف',
    onSuccess: () => {
      programsElement.value = programsElement.value.filter((p) => p.id !== id)
      if (currentProgramElementId.value === id) {
        currentProgramElementId.value = null
        formProgramElement.value = {}
      }
    },
  })

// ==============================================
// ================ 3️⃣ WORKFLOWS ===============
// ==============================================

const loadWorkflows = async () => {
  try {
    const { data } = await automationService.listWorkflows()
    workflows.value = data
  } catch (err) {
    showToast('error', 'فشل تحميل الـ Workflows', err?.message)
  } finally {
    loadingWorkflows.value = false
  }
}

const loadWorkflowEvents = async (workflowId) => {
  if (!workflowId) return
  nodes.value = []
  edges.value = []
  const { data: wfData } = await automationService.getWorkflow(workflowId)
  currentWorkflowId.value = wfData.id
  formWorkflow.value = { name: wfData.name, description: wfData.description, status: wfData.status }
  try {
    const { data } = await automationService.getWorkflow_full_events(workflowId)
    nodes.value = (data.nodes || []).map((n) => ({
      id: n.id,
      type: 'custom',
      position: n.position || {
        x: n.data?.node?.position_x ?? 0,
        y: n.data?.node?.position_y ?? 0,
      },
      data: {
        label: n.data?.label ?? n.data?.node?.label ?? '',
        node: {
          backend_id: n.id,
          id: n.id,
          program_name: n.data?.node?.program_name ?? '',
          element_name: n.data?.node?.element_name ?? '',
          node_type: n.data?.node?.node_type ?? '',
          label: n.data?.node?.label ?? '',
          config: n.data?.node?.config ?? null,
          program: n.data?.node?.program ?? null,
          element: n.data?.node?.element ?? null,
          status: 'idle',
        },
        actions: n.data?.actions ?? [],
      },
    }))
    edges.value = (data.edges || []).map((e) => ({
      id: e.id,
      source: e.source,
      target: e.target,
      type: e.type || 'custom',
      data: e.data || {},
    }))
  } catch (err) {
    showToast('error', 'فشل تحميل الـ Workflow Events', err?.message)
  }
}

const selectWorkflow = async (id) => {
  if (!id) return
  isLoadingWorkflow.value = true
  debouncedAutoSave.cancel()
  currentWorkflowId.value = id
  await loadWorkflowEvents(id)
  isLoadingWorkflow.value = false
}

const createWorkflow = () =>
  workflowAction.run(
    () => {
      if (!formWorkflow.value.name?.trim()) {
        showToast('warn', 'الاسم مطلوب', 'أدخل اسم الـ Workflow')
        throw new Error('Name required')
      }
      return automationService.createWorkflow({
        name: formWorkflow.value.name,
        description: formWorkflow.value.description,
        status: formWorkflow.value.status,
      })
    },
    {
      successSummary: 'تم إنشاء الـ Workflow',
      errorSummary: 'فشل إنشاء الـ Workflow',
      onSuccess: async ({ data }) => {
        workflows.value.unshift(data)
        currentWorkflowId.value = data.id
        nodes.value = []
        edges.value = []
        await loadWorkflowEvents(data.id)
      },
    },
  )

const saveWorkflow = async () => {
  if (!currentWorkflowId.value || isLoadingWorkflow.value || isSavingWorkflow.value) return
  const exists = workflows.value.find((w) => w.id === currentWorkflowId.value)
  if (!exists) return

  isSavingWorkflow.value = true
  isLoadingWorkflow.value = true
  debouncedAutoSave.cancel()
  const openNodeLabel = showActionPanel.value
    ? (selectedNode.value?.data?.node?.label ?? null)
    : null

  try {
    await automationService.saveWorkflowAll(currentWorkflowId.value, {
      nodes: nodes.value.map((n) => ({
        id: n.id,
        position: n.position,
        data: n.data,
        actions: n.data?.actions ?? [],
      })),
      edges: edges.value.map((e) => ({
        id: e.id,
        source: e.source,
        target: e.target,
        data: e.data,
      })),
    })
    await loadWorkflowEvents(currentWorkflowId.value)
    if (openNodeLabel && showActionPanel.value) {
      const refreshed = nodes.value.find((n) => n.data?.node?.label === openNodeLabel)
      if (refreshed) selectedNode.value = refreshed
    }
    toast.add({ severity: 'success', summary: '✅ Saved', detail: 'Workflow saved', life: 2000 })
  } catch (err) {
    showToast('error', 'فشل الحفظ', err?.message)
  } finally {
    isLoadingWorkflow.value = false
    isSavingWorkflow.value = false
  }
}

const updateStatusWorkflow = (status) =>
  workflowAction.run(() => automationService.updateWorkflow(currentWorkflowId.value, { status }), {
    successSummary: 'تم تحديث الحالة',
    successDetail: `Status: ${status}`,
    errorSummary: 'فشل تحديث الحالة',
    onSuccess: () => {
      const wf = workflows.value.find((w) => w.id === currentWorkflowId.value)
      if (wf) wf.status = status
    },
  })

const deleteWorkflow = (id) =>
  workflowAction.run(() => automationService.deleteWorkflow(id), {
    successSummary: 'تم الحذف',
    errorSummary: 'فشل الحذف',
    onSuccess: async () => {
      workflows.value = workflows.value.filter((w) => w.id !== id)
      if (currentWorkflowId.value === id) {
        currentWorkflowId.value = null
        nodes.value = []
        edges.value = []
      }
      await loadWorkflows()
    },
  })

const clearWorkflow = () => {
  nodes.value = []
  edges.value = []
}

// ==============================================
// 📐 AUTO LAYOUT (Dagre)
// ==============================================
function autoLayout(dir = 'TB') {
  isLayoutingWorkflow.value = true
  const g = new dagre.graphlib.Graph()
  g.setGraph({ rankdir: dir, nodesep: 50, ranksep: 80 })
  g.setDefaultEdgeLabel(() => ({}))
  nodes.value.forEach((n) => g.setNode(n.id, { width: 180, height: 60 }))
  edges.value.forEach((e) => g.setEdge(e.source, e.target))
  dagre.layout(g)
  nodes.value = nodes.value.map((node) => {
    const pos = g.node(node.id)
    return { ...node, position: { x: pos.x - 90, y: pos.y - 30 } }
  })
  setTimeout(() => {
    isLayoutingWorkflow.value = false
  }, 400)
}

// ==============================================
// =================== 4️⃣ Nodes ================
// ==============================================

const loadlistWorkflowNodes = async () => {
  try {
    const { data } = await automationService.listWorkflowNodes()
    nodes.value = data.map((n) => ({
      ...n,
      type: 'custom',
      position: { x: n.position_x, y: n.position_y },
      data: n.data,
    }))
    nodes.value.forEach((n) => workflowState.nodesMap.set(n.id, n))
  } catch (err) {
    console.error('Error loading nodes:', err)
  }
}

const loadNode = async (id) => {
  const { data } = await automationService.getWorkflowNode(id)
  currentNodeId.value = data.id
}

const getFreshNode = (nodeId) =>
  nodes.value.find((n) => n.id === nodeId || n.data?.node?.backend_id === nodeId) ??
  selectedNode.value

const onNodeSelect = async ({ node }) => {
  const freshNode = getFreshNode(node.id)
  selectedNode.value = freshNode ?? node
  showActionPanel.value = true
  if (node.id) await loadNode(node.id)
}

const createNode = async (item, dropEvent) => {
  if (!currentWorkflowId.value) {
    showToast('warn', 'لا يوجد Workflow', 'اختر Workflow الأول')
    return
  }
  isLoadingWorkflow.value = true
  debouncedAutoSave.cancel()
  try {
    const position = project({ x: dropEvent.clientX, y: dropEvent.clientY })
    const actionMap = { program: 'open_program', 'program-element': 'press', delay: 'wait' }
    const actionType = actionMap[item.type] || 'custom'
    await loadProgram(item.id)
    const uiConfig = {
      ui: {
        theme: { background: '#0f172a', border: '#334155', shadow: '#334155' },
        layout: { width: 260, height: 240, rounded: true },
      },
      inputs: [
        { key: 'text', label: 'Text', type: 'string', value: '' },
        { key: 'delay', label: 'Delay (ms)', type: 'number', value: 0 },
        { key: 'color', label: 'Background Color', type: 'color', value: '#0f172a' },
      ],
      ai: { enabled: false, context: {}, memory: [], suggestions: [] },
    }
    const { data: nodeData } = await automationService.createWorkflowNode({
      workflow: currentWorkflowId.value,
      node_type: item.type,
      label: actionType || 'New Node',
      program: item.type === 'program' ? item.id : null,
      element: item.type === 'program-element' ? item.id : null,
      position_x: position.x,
      position_y: position.y,
      config: uiConfig,
    })
    const actionResponse = await createAction({
      node: nodeData.id,
      action_type: actionType,
      payload: {},
    })
    nodes.value.push({
      id: nodeData.id,
      type: 'custom',
      position: { x: nodeData.position_x, y: nodeData.position_y },
      data: {
        label: nodeData.label,
        node: {
          backend_id: nodeData.id,
          id: nodeData.id,
          program_name: nodeData.program_name,
          element_name: nodeData.element_name,
          node_type: nodeData.node_type,
          label: nodeData.label,
          config: nodeData.config,
          program: nodeData.program,
          element: nodeData.element,
          status: 'idle',
        },
        actions: actionResponse ? [actionResponse] : [],
      },
    })
    toast.add({
      severity: 'success',
      summary: `✅ Node Created`,
      detail: nodeData.label,
      life: 3000,
    })
  } catch (err) {
    showToast('error', 'فشل إنشاء الـ Node', err?.message)
  } finally {
    isLoadingWorkflow.value = false
  }
}

const enqueueUpdate = (job) => {
  workflowState.updateQueue.push(job)
  debouncedSync()
}
const processQueue = async () => {
  if (workflowState.isSyncing) return
  workflowState.isSyncing = true
  while (workflowState.updateQueue.length > 0) {
    const job = workflowState.updateQueue.shift()
    try {
      if (job.type === 'node-position')
        await automationService.updateWorkflowNode(job.id, {
          position_x: job.position_x,
          position_y: job.position_y,
        })
      if (job.type === 'node-config') await automationService.updateWorkflowNode(job.id, job.data)
      if (job.type === 'action') await automationService.updateAction(job.id, job.data)
    } catch (err) {
      console.error('Sync error:', err)
    }
  }
  workflowState.isSyncing = false
}
const debouncedSync = debounce(() => processQueue(), 300)

const startDrag = (item) => {
  draggedItem.value = item
}
const onDragOver = (e) => {
  e.preventDefault()
  e.dataTransfer.dropEffect = 'move'
}
const onDrop = async (e) => {
  e.preventDefault()
  if (!draggedItem.value) return
  await createNode(draggedItem.value, e)
  draggedItem.value = null
}

const runTaskFromNode = async (nodeData) => {
  const backendId = nodeData?.backend_id
  if (!backendId) {
    showToast('error', 'Node Error', 'Backend ID not found')
    return
  }
  try {
    await automationService.runWorkflowNode(backendId)
    const action = nodeData.config?.action || 'open'
    if (action === 'open') openProgram(nodeData.programId)
    else if (action === 'close') closeProgram(nodeData.programId)
    else if (action === 'status') statusProgram(nodeData.programId)
    else if (action === 'focus') focusProgram(nodeData.programId)
    else if (action === 'maximize') maximizeProgram(nodeData.programId)
    toast.add({ severity: 'success', summary: 'Node Running', detail: 'Task executed', life: 2500 })
  } catch (err) {
    showToast('error', 'Execution Failed', err.response?.data || err.message)
  }
}

const deleteNodeOnWorkflow = async (id) => {
  if (!id) return
  try {
    await automationService.deleteWorkflowNode(id)
    nodes.value = nodes.value.filter((n) => n.id !== id)
    edges.value = edges.value.filter((e) => e.source !== id && e.target !== id)
    toast.add({ severity: 'success', summary: '✅ Deleted', life: 3000 })
  } catch (err) {
    showToast('error', 'فشل الحذف', err?.message)
  }
}

const createNodeAction = async ({ nodeId, action_type }) => {
  const freshNode = getFreshNode(nodeId)
  const realId = freshNode?.data?.node?.backend_id ?? freshNode?.id
  if (!realId) {
    showToast('error', 'Node ID missing', '')
    return
  }
  try {
    const actionResponse = await createAction({
      node: realId,
      action_type,
      payload: {
        ai: { memory: [], context: {}, enabled: false, suggestions: [] },
        ui: {
          theme: { border: '#334155', shadow: '#334155', background: '#0f172a' },
          layout: { width: 260, height: 240, rounded: true },
        },
        inputs: [
          { key: 'text', type: 'string', label: 'Text', value: '' },
          { key: 'delay', type: 'number', label: 'Delay (ms)', value: 0 },
          { key: 'color', type: 'color', label: 'Background Color', value: '#0f172a' },
        ],
      },
    })
    if (!actionResponse) return
    const idx = nodes.value.findIndex((n) => n.id === realId || n.data?.node?.backend_id === realId)
    if (idx !== -1) {
      nodes.value[idx] = {
        ...nodes.value[idx],
        data: {
          ...nodes.value[idx].data,
          actions: [...(nodes.value[idx].data.actions ?? []), actionResponse],
        },
      }
      selectedNode.value = nodes.value[idx]
    }
    toast.add({
      severity: 'success',
      summary: '✅ Action Created',
      detail: action_type,
      life: 2000,
    })
  } catch (err) {
    showToast('error', 'فشل إنشاء الـ Action', err?.message)
  }
}

const updateNodeAction = async ({ nodeId, actionId, newActionType }) => {
  try {
    const payload = buildPayloadFromUI(newActionType, {})
    const idx = nodes.value.findIndex((n) => n.id === nodeId)
    if (idx !== -1) {
      const updated = { ...nodes.value[idx], data: { ...nodes.value[idx].data } }
      updated.data.actions = updated.data.actions.map((a) =>
        a.id === actionId ? { ...a, action_type: newActionType, payload } : a,
      )
      nodes.value[idx] = updated
      selectedNode.value = nodes.value[idx]
    }
    await automationService.updateAction(actionId, { action_type: newActionType, payload })
    toast.add({
      severity: 'success',
      summary: '✅ Action Updated',
      detail: newActionType,
      life: 2000,
    })
  } catch (err) {
    showToast('error', 'فشل تحديث الـ Action', err?.message)
  }
}

const deleteNodeAction = async ({ nodeId, actionId }) => {
  try {
    await automationService.deleteAction(actionId)
    const idx = nodes.value.findIndex((n) => n.id === nodeId)
    if (idx !== -1) {
      const updated = { ...nodes.value[idx], data: { ...nodes.value[idx].data } }
      updated.data.actions = updated.data.actions.filter((a) => a.id !== actionId)
      nodes.value[idx] = updated
      selectedNode.value = nodes.value[idx]
    }
    toast.add({ severity: 'success', summary: '🗑️ Deleted', life: 2000 })
  } catch (err) {
    showToast('error', 'فشل الحذف', err?.message)
  }
}

// ==============================================
// =================== 5️⃣ Edges ================
// ==============================================
const onConnect = async (params) => {
  if (!currentWorkflowId.value) return
  try {
    const { data } = await automationService.createWorkflowEdge({
      workflow: currentWorkflowId.value,
      source_node: params.source,
      target_node: params.target,
      condition: 'success',
    })
    edges.value.push({
      id: data.id,
      source: data.source_node,
      target: data.target_node,
      sourceHandle: 'source',
      targetHandle: 'target',
      type: 'default',
      data: { label: data.condition },
      animated: true,
      style: { stroke: '#4CAF50', strokeWidth: 2 },
    })
    toast.add({ severity: 'success', summary: '✅ Edge Created', life: 2500 })
  } catch (err) {
    showToast('error', 'فشل إنشاء الـ Edge', err?.message)
  }
}

const onNodeDragStop = (node) => {
  const backendId = node.data?.node?.backend_id ?? node.id
  if (!backendId) return
  enqueueUpdate({
    type: 'node-position',
    id: backendId,
    position_x: node.position.x,
    position_y: node.position.y,
  })
}

const startWorkflow = () =>
  workflowAction.run(
    () => {
      if (!currentWorkflowId.value) {
        showToast('warn', 'لا يوجد Workflow', 'اختر Workflow الأول')
        throw new Error()
      }
      return automationService.runWorkflow(currentWorkflowId.value)
    },
    {
      successSummary: '🚀 Workflow Started',
      successDetail: 'Workflow Started successfully',
      errorSummary: 'فشل تشغيل الـ Workflow',
      onSuccess: ({ data }) => {
        currentTaskRunId.value = data.task_run_id
      },
    },
  )

// ==============================================
// ================== 6️⃣ Actions ===============
// ==============================================
const createAction = async ({ node, action_type, payload }) => {
  try {
    const res = await automationService.createAction({ node, action_type, payload })
    toast.add({
      severity: 'success',
      summary: `✅ Action created`,
      detail: action_type,
      life: 3000,
    })
    return res.data
  } catch (err) {
    showToast('error', 'فشل إنشاء الـ Action', err?.message)
    console.error('createAction details:', err.response?.data)
  }
}

const buildPayloadFromUI = (type, extraData = {}) =>
  ({
    wait: { seconds: Number(extraData.delay || 0) },
    press: { key: extraData.key },
    hotkey: { keys: extraData.keys },
    click_element: { element_id: extraData.element_id },
    open_program: {},
  })[type] || {}

const handleUpdateNodeAction = async ({ nodeId, newActionType, extraData }) => {
  const node = workflowState.nodesMap.get(nodeId)
  if (!node) return
  const payload = buildPayloadFromUI(newActionType, extraData)
  node.data.actions.action_type = newActionType
  node.data.actions.payload = payload
  nodes.value = [...nodes.value]
  workflowState.updateQueue.push({
    type: 'action',
    nodeId,
    actionId: node.data.actions.id,
    action_type: newActionType,
    payload,
  })
  syncWithBackend()
}

const syncWithBackend = async () => {
  if (workflowState.isSyncing) return
  workflowState.isSyncing = true
  while (workflowState.updateQueue.length) {
    const job = workflowState.updateQueue.shift()
    try {
      if (job.type === 'action')
        await automationService.updateAction(job.actionId, {
          action_type: job.action_type,
          payload: job.payload,
        })
      if (job.type === 'node-position')
        await automationService.updateWorkflowNode(job.nodeId, job.data)
    } catch (err) {
      console.error('Sync failed:', err)
    }
  }
  workflowState.isSyncing = false
}

// ==============================================
// ================== 7️⃣ Tasks =================
// ==============================================
const loadTasks = async () => {
  loadingTasks.value = true
  try {
    const { data } = await automationService.listTasks()
    tasks.value = data
  } catch (err) {
    showToast('error', 'فشل تحميل الـ Tasks', err?.message)
  } finally {
    loadingTasks.value = false
  }
}

const selectTask = async (id) => {
  if (!id) return
  currentTaskId.value = id
  await loadTask(id)
}
const loadTask = async (id) => {
  const { data } = await automationService.getTask(id)
  currentTaskId.value = data.id
  formTask.value = { name: data.name, description: data.description, program: data.program }
}

// CREATE Task — same pattern
const createTask = () =>
  taskAction.run(
    () => {
      const err = validateTask(formTask.value)
      if (err) {
        showToast('warn', 'تحقق من البيانات', err)
        throw new Error(err)
      }
      const fd = new FormData()
      fd.append('name', formTask.value.name)
      fd.append('description', formTask.value.description)
      fd.append('program', formTask.value.program)
      return automationService.createTask(fd)
    },
    {
      successSummary: 'تم إنشاء الـ Task',
      errorSummary: 'فشل إنشاء الـ Task',
      onSuccess: async ({ data }) => {
        tasks.value.unshift(data)
        currentTaskId.value = data.id
        ceateTaskVisible.value = false // ✅ closes ONLY on success
        await loadTasks()
      },
    },
  )

const openEditTask = async (id) => {
  if (!id) return
  try {
    currentProgramElementId.value = id
    await loadProgramElement(id)
    editProgramElementsVisible.value = true
  } catch (err) {
    showToast('error', 'فشل تحميل البيانات', err?.message)
  }
}

const editTask = () =>
  taskAction.run(
    () => {
      const fd = new FormData()
      fd.append('name', formProgramElement.value.name)
      fd.append('description', formProgram.value.description)
      fd.append('program', formProgramElement.value.program)
      if (formProgramElement.value.image instanceof File)
        fd.append('image', formProgramElement.value.image)
      return automationService.updateProgramElement(currentProgramElementId.value, fd)
    },
    {
      successSummary: 'تم تحديث الـ Task',
      errorSummary: 'فشل تحديث الـ Task',
      onSuccess: async () => {
        editTaskVisible.value = false // ✅ closes ONLY on success
        await loadProgramElements()
      },
    },
  )

const confirmDeleteTask = (task) => {
  confirm.require({
    message: `هل أنت متأكد من حذف "${task.name}"؟`,
    header: '⚠️ تأكيد الحذف',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'نعم، احذف',
    rejectLabel: 'إلغاء',
    accept: () => deleteTask(task.id),
  })
}
const deleteTask = (id) =>
  taskAction.run(() => automationService.deleteTask(id), {
    successSummary: 'تم الحذف',
    errorSummary: 'فشل الحذف',
    onSuccess: () => {
      programsElement.value = programsElement.value.filter((p) => p.id !== id)
      if (currentProgramElementId.value === id) {
        currentProgramElementId.value = null
        formProgramElement.value = {}
      }
    },
  })

// ==============================================
// ================== 🔟 Delays ================
// ==============================================
const loadDelays = async () => {
  loadingDelays.value = true
  try {
    const { data } = await automationService.listDelays()
    delays.value = data
  } catch (err) {
    console.error('Error loading delays:', err)
  } finally {
    loadingDelays.value = false
  }
}

// ==============================================
// ================== Auto Save ================
// ==============================================
const debouncedAutoSave = debounce(() => {
  if (!isInitialized.value || !currentWorkflowId.value || isLoadingWorkflow.value) return
  if (currentProgramId.value) formProgramElement.value.program = currentProgramId.value
  const exists = workflows.value.find((w) => w.id === currentWorkflowId.value)
  if (!exists) return
  saveWorkflow()
}, 500)

watch([nodes, edges], debouncedAutoSave, { deep: true })
watch(currentProgramId, (newId) => {
  if (newId) formProgramElement.value.program = newId
})

onMounted(async () => {
  await Promise.all([
    loadPrograms(),
    loadProgramElements(),
    loadWorkflows(),
    loadlistWorkflowNodes(),
    loadDelays(),
    loadTasks(),
  ])
  isInitialized.value = true
  if (currentWorkflowId.value) await loadWorkflowEvents(currentWorkflowId.value)
})
</script>

<template>
  <main class="h-screen p-4">
    <div class="grid grid-cols-12 gap-4 h-full">
      <aside class="col-span-3 border rounded p-4 overflow-auto space-y-6">
        <div>
          <div class="flex justify-between items-center my-3">
            <h3 class="text-lg font-bold">
              <prime_tag value="🖥️ Programs" />
            </h3>
            <prime_button
              icon="pi pi-plus"
              @click="ceateProgramVisible = true"
              :disabled="programAction.loading.value"
              style="background-color: transparent; padding: 0; border: none"
            >
              <prime_tag icon="pi pi-plus" />
            </prime_button>
          </div>
          <div class="wrapper_programs">
            <div v-if="loadingPrograms">
              <prime_skeleton
                height="3rem"
                width="100%"
                class="mt-2"
                shape="circle"
                borderRadius="16px"
              />
              <prime_skeleton
                height="3rem"
                width="100%"
                class="mt-2"
                shape="circle"
                borderRadius="16px"
              />
              <prime_skeleton
                height="3rem"
                width="100%"
                class="mt-2"
                shape="circle"
                borderRadius="16px"
              />
            </div>
            <div
              v-for="p in programs"
              :key="p.id"
              class="p-1 rounded cursor-grab link_aside"
              draggable="true"
              @dragstart="startDrag({ type: 'program', id: p.id })"
              v-else
              @click="selectProgram(p.id)"
            >
              <prime_image alt="Image" preview>
                <template #previewicon><i class="pi pi-search"></i></template>
                <template #image><img :src="p.get_image" alt="image" /></template>
                <template #preview="slotProps"
                  ><img
                    :src="p.get_image"
                    alt="preview"
                    :style="slotProps.style"
                    @click="slotProps.onClick"
                /></template>
              </prime_image>
              <prime_tag :value="p.name" />
              <div>
                <prime_button
                  icon="pi pi-plus"
                  @click.stop="openEditProgram(p.id)"
                  style="background-color: transparent; padding: 0; border: none"
                  ><prime_tag icon="pi pi-file-edit"
                /></prime_button>
                <prime_button
                  icon="pi pi-plus"
                  @click.stop="confirmDeleteProgram(p)"
                  style="background-color: transparent; padding: 0; border: none"
                  ><prime_tag icon="pi pi-trash"
                /></prime_button>
              </div>
            </div>
          </div>
        </div>

        <div>
          <div class="flex justify-between items-center my-3">
            <h3 class="text-lg font-bold"><prime_tag value="🧩 Program Elements" /></h3>
            <prime_button
              icon="pi pi-plus"
              @click="ceateProgramElementsVisible = true"
              style="background-color: transparent; padding: 0; border: none"
              ><prime_tag icon="pi pi-plus"
            /></prime_button>
          </div>
          <div class="wrapper_programs">
            <div v-if="loadingProgramElements">
              <prime_skeleton
                height="3rem"
                width="100%"
                class="mt-2"
                shape="circle"
                borderRadius="16px"
              />
              <prime_skeleton
                height="3rem"
                width="100%"
                class="mt-2"
                shape="circle"
                borderRadius="16px"
              />
            </div>
            <div
              v-for="p in programsElement"
              :key="p.id"
              class="p-1 rounded cursor-grab link_aside"
              draggable="true"
              @dragstart="startDrag({ type: 'program-element', id: p.id })"
              v-else
              @click="selectProgramElement(p.id)"
            >
              <prime_image alt="Image" preview>
                <template #previewicon><i class="pi pi-search"></i></template>
                <template #image><img :src="p.get_image" alt="image" /></template>
                <template #preview="slotProps"
                  ><img
                    :src="p.get_image"
                    alt="preview"
                    :style="slotProps.style"
                    @click="slotProps.onClick"
                /></template>
              </prime_image>
              <prime_tag :value="p.name" />
              <div>
                <prime_button
                  icon="pi pi-plus"
                  @click.stop="openEditProgramElement(p.id)"
                  style="background-color: transparent; padding: 0; border: none"
                  ><prime_tag icon="pi pi-file-edit"
                /></prime_button>
                <prime_button
                  icon="pi pi-plus"
                  @click.stop="confirmDeleteProgramElement(p)"
                  style="background-color: transparent; padding: 0; border: none"
                  ><prime_tag icon="pi pi-trash"
                /></prime_button>
              </div>
            </div>
          </div>
        </div>

        <div>
          <div class="flex justify-between items-center my-3">
            <h3 class="text-lg font-bold"><prime_tag value="Delays" /></h3>
            <RouterLink to="/"><prime_tag icon="pi pi-plus" /></RouterLink>
          </div>
          <div class="wrapper_delays">
            <div v-if="loadingDelays">
              <prime_skeleton
                height="3rem"
                width="100%"
                class="mt-2"
                shape="circle"
                borderRadius="16px"
              />
              <prime_skeleton
                height="3rem"
                width="100%"
                class="mt-2"
                shape="circle"
                borderRadius="16px"
              />
            </div>
            <div
              v-for="d in delays"
              :key="d.id"
              class="p-2 rounded cursor-grab link_aside"
              draggable="true"
              @dragstart="startDrag({ type: 'delay', id: d.id })"
              v-else
            >
              <i class="pi pi-stopwatch"></i>
              <prime_tag :value="d.seconds + 's'" />
              <prime_tag value="Delay" />
            </div>
          </div>
        </div>

        <div>
          <h3 class="text-lg font-bold mb-3">Workflows</h3>
          <div class="space-y-2">
            <div
              v-for="w in workflows"
              :key="w.id"
              class="p-2 bg-white border rounded cursor-pointer align-content-between"
              @click="selectWorkflow(w.id)"
            >
              <span>{{ w.name }}</span>
              <span
                class="text-xs px-2 py-1 rounded"
                :class="{
                  'bg-gray-200': w.status === 'draft',
                  'bg-green-200': w.status === 'active',
                  'bg-yellow-200': w.status === 'paused',
                }"
                >{{ w.status }}</span
              >
            </div>
          </div>
        </div>

        <div>
          <div class="flex justify-between items-center mb-3">
            <h3 class="text-lg font-bold"><prime_tag value="Tasks Templates" /></h3>
            <prime_button
              icon="pi pi-plus"
              @click="ceateTaskVisible = true"
              style="background-color: transparent; padding: 0; border: none"
              ><prime_tag icon="pi pi-plus"
            /></prime_button>
          </div>
          <div class="wrapper_programs">
            <div v-if="loadingTasks">
              <prime_skeleton
                height="3rem"
                width="100%"
                class="mt-2"
                shape="circle"
                borderRadius="16px"
              />
              <prime_skeleton
                height="3rem"
                width="100%"
                class="mt-2"
                shape="circle"
                borderRadius="16px"
              />
            </div>
            <div
              v-for="t in tasks"
              :key="t.id"
              class="p-1 rounded cursor-grab link_aside"
              draggable="true"
              @dragstart="startDrag({ type: 'task', id: t.id })"
              v-else
              @click="selectTask(t.id)"
            >
              <prime_tag :value="t.name" />
              <div>
                <prime_button
                  icon="pi pi-plus"
                  @click.stop="openEditTask(t.id)"
                  style="background-color: transparent; padding: 0; border: none"
                  ><prime_tag icon="pi pi-file-edit"
                /></prime_button>
                <prime_button
                  icon="pi pi-plus"
                  @click.stop="confirmDeleteTask(t)"
                  style="background-color: transparent; padding: 0; border: none"
                  ><prime_tag icon="pi pi-trash"
                /></prime_button>
              </div>
            </div>
          </div>
        </div>

        <div>
          <vuedraggable :list="programs" group="tasks" class="draggable-list">
            <template #item="{ element }">
              <div
                class="draggable-item"
                draggable="true"
                @dragstart="(event) => onDragStart(event, element)"
              >
                <div
                  v-for="p in programs"
                  :key="p.id"
                  class="p-1 rounded cursor-grab link_aside"
                  draggable="true"
                  @dragstart="startDrag({ type: 'program', id: p.id })"
                  @click="selectProgram(p.id)"
                >
                  <prime_image alt="Image" preview>
                    <template #previewicon><i class="pi pi-search"></i></template>
                    <template #image><img :src="p.get_image" alt="image" /></template>
                    <template #preview="slotProps"
                      ><img
                        :src="p.get_image"
                        alt="preview"
                        :style="slotProps.style"
                        @click="slotProps.onClick"
                    /></template>
                  </prime_image>
                  <prime_tag :value="p.name" />
                  <div>
                    <prime_button
                      icon="pi pi-plus"
                      @click.stop="openEditProgram(p.id)"
                      style="background-color: transparent; padding: 0; border: none"
                      ><prime_tag icon="pi pi-file-edit"
                    /></prime_button>
                    <prime_button
                      icon="pi pi-plus"
                      @click.stop="confirmDeleteProgram(p)"
                      style="background-color: transparent; padding: 0; border: none"
                      ><prime_tag icon="pi pi-trash"
                    /></prime_button>
                  </div>
                </div>
              </div>
            </template>
          </vuedraggable>
        </div>
      </aside>

      <section class="col-span-9 mb-16">
        <div class="wrapper_name_description">
          <div class="inner_name_description">
            <div>
              <label class="block font-semibold mb-1">Name</label>
              <input
                v-model="formWorkflow.name"
                type="text"
                class="input"
                placeholder="Program name"
              />
            </div>
            <div>
              <label class="block font-semibold mb-1">Description</label>
              <textarea
                v-model="formWorkflow.description"
                placeholder="Program description"
                class="textarea"
                cols="30"
                rows="1"
              ></textarea>
            </div>
            <div>
              <label class="block font-semibold mb-1">Status</label>
              <select v-model="formWorkflow.status" class="input">
                <option value="draft">📝 Draft</option>
                <option value="active">✅ Active</option>
                <option value="paused">⏸ Paused</option>
              </select>
            </div>
            <div>
              <prime_button
                label="🗑️"
                @click="deleteWorkflow(currentWorkflowId)"
                :loading="workflowAction.loading.value"
                class="class_name"
              />
            </div>
          </div>
        </div>

        <VueFlow
          class="border rounded"
          v-model:nodes="nodes"
          v-model:edges="edges"
          :node-types="nodeTypes"
          :edge-types="edgeTypes"
          @node-click="onNodeSelect"
          @dragover="onDragOver"
          @drop="onDrop"
          @connect="onConnect"
          @nodeDragStop="onNodeDragStop"
          :pan-on-drag="[1]"
          :pan-on-scroll="true"
          :zoom-on-scroll="false"
        >
          <Background variant="dots" pattern-color="#aaa" :gap="10" />
          <Controls />
          <template #node-custom="props">
            <CustomNode
              v-bind="props"
              @run-task="runTaskFromNode"
              @open-program="openProgram"
              @close-program="closeProgram"
              @status-program="statusProgram"
              @delete-node="deleteNodeOnWorkflow"
              @update-node-action="handleUpdateNodeAction"
            />
          </template>
          <template #edge-custom="props"><CustomEdge v-bind="props" /></template>
          <MiniMap />
          <Panel position="top-left">
            <div class="flex gap-2">
              <button
                @click="createWorkflow"
                :disabled="workflowAction.loading.value"
                class="btn-white"
              >
                ➕ إنشاء Workflow جديد
              </button>
              <button @click="saveWorkflow" :disabled="isSavingWorkflow" class="btn-white">
                {{ isSavingWorkflow ? '⏳ جاري الحفظ…' : '💾 Save Workflow' }}
              </button>
              <button @click="clearWorkflow" class="btn-white">🗑️ مسح الكل</button>
              <button
                @click="updateStatusWorkflow('active')"
                :disabled="workflowAction.loading.value"
              >
                ▶ Activate
              </button>
              <button
                @click="updateStatusWorkflow('paused')"
                :disabled="workflowAction.loading.value"
              >
                ⏸ Pause
              </button>
              <prime_button
                label="Start Workflow"
                icon="pi pi-play"
                class="p-button-success"
                :disabled="!currentWorkflowId || workflowAction.loading.value"
                :loading="workflowAction.loading.value"
                @click.once="startWorkflow"
              />
            </div>
            <div class="inner_control_node_layout_buttons">
              <button @click="autoLayout('LR')">LR 📐</button>
              <button @click="autoLayout('RL')">RL 📐</button>
              <button @click="autoLayout('TB')">TB 📐</button>
              <button @click="autoLayout('BT')">BT 📐</button>
            </div>
          </Panel>
        </VueFlow>
      </section>
    </div>

    <LiveConsole v-if="taskRunId" :taskRunId="currentTaskRunId" />

    <ApiFlowPanel :stages="stages" :meta="meta" :error="trackerError" :show-data="true" />
    <ApiFlowPanel :stages="stages" :meta="meta" :error="error" :show-data="true" />

    <ActionPanel
      :show="showActionPanel"
      :selected-node="selectedNode"
      v-model:new-action-type-for-panel="newActionTypeForPanel"
      @close="showActionPanel = false"
      @create-action="createNodeAction"
      @update-action="updateNodeAction"
      @delete-action="deleteNodeAction"
    />

    <CreateProgram
      v-model:visible="ceateProgramVisible"
      :form="formProgram"
      :loading="programAction.loading.value"
      @image-change="onImageChangeProgram"
      @submit="createProgram"
    />

    <div class="card flex justify-center">
      <prime_dialog
        v-model:visible="editProgramVisible"
        pt:root:class="!border-0 !bg-transparent"
        pt:mask:class="backdrop-blur-sm"
      >
        <template #container="{ closeCallback }">
          <div
            class="flex flex-col px-8 py-8 gap-6 rounded-2xl"
            style="
              background-image: radial-gradient(
                circle at left top,
                var(--p-primary-400),
                var(--p-primary-700)
              );
            "
          >
            <div style="margin: auto; font-size: 2rem; font-weight: bolder">Edit Program</div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold"
                  >Program Name <span class="text-red-300">*</span></label
                >
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.name"
                  type="text"
                  placeholder="Program name"
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Description</label>
                <prime_textarea
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.description"
                  placeholder="Program description"
                />
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold"
                  >Executable Path <span class="text-red-300">*</span></label
                >
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.executable_path"
                  type="text"
                  placeholder="C:/Program Files/VSCode/Code.exe"
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Project Path</label>
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.project_path"
                  type="text"
                  placeholder="C:/Users/project"
                />
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Working Directory</label>
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.working_directory"
                  type="text"
                  placeholder="C:/Users/project"
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Window Title Pattern</label>
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgram.window_title_pattern"
                  type="text"
                  placeholder="Project Name"
                />
              </div>
            </div>
            <div><input type="file" accept="image/*" @change="onImageChangeProgram" /></div>
            <div class="flex items-center gap-4">
              <prime_button
                label="Cancel"
                @click="closeCallback"
                variant="text"
                :disabled="programAction.loading.value"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
              <prime_button
                :label="programAction.loading.value ? 'جاري التحديث…' : 'Update'"
                :loading="programAction.loading.value"
                :disabled="programAction.loading.value"
                @click="editProgram"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
            </div>
          </div>
        </template>
      </prime_dialog>
    </div>

    <div class="card flex justify-center" style="overflow-y: auto">
      <prime_dialog
        v-model:visible="ceateProgramElementsVisible"
        pt:root:class="!border-0 !bg-transparent"
        pt:mask:class="backdrop-blur-sm"
      >
        <template #container="{ closeCallback }">
          <div
            class="flex flex-col px-8 py-8 gap-6 rounded-2xl"
            style="
              background-image: radial-gradient(
                circle at left top,
                var(--p-primary-400),
                var(--p-primary-700)
              );
            "
          >
            <div style="margin: auto; font-size: 2rem; font-weight: bolder">
              Create Program Element
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold"
                  >Name <span class="text-red-300">*</span></label
                >
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.name"
                  placeholder="Element name"
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Description</label>
                <prime_textarea
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.description"
                  placeholder="Description"
                />
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Image</label>
                <input type="file" accept="image/*" @change="onImageChangeProgramElement" />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold"
                  >Program <span class="text-red-300">*</span></label
                >
                <select v-model="formProgramElement.program" class="input">
                  <option disabled value="">اختر البرنامج</option>
                  <option v-for="p in programs" :key="p.id" :value="p.id">{{ p.name }}</option>
                </select>
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold"
                  >Selector Type <span class="text-red-300">*</span></label
                >
                <select v-model="formProgramElement.selector_type">
                  <option disabled value="">Choose selector type</option>
                  <option
                    v-for="type in programElementselectorTypes"
                    :key="type.value"
                    :value="type.value"
                  >
                    {{ type.label }}
                  </option>
                </select>
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <prime_input_text
                class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                v-model="formProgramElement.x"
                placeholder="X"
              />
              <prime_input_text
                class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                v-model="formProgramElement.y"
                placeholder="Y"
              />
            </div>
            <div class="inline-flex flex-row gap-2">
              <prime_input_text
                class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                v-model="formProgramElement.width"
                placeholder="Width"
              />
              <prime_input_text
                class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                v-model="formProgramElement.height"
                placeholder="Height"
              />
            </div>
            <div class="inline-flex flex-row gap-2">
              <prime_input_text
                class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                v-model="formProgramElement.shortcut"
                placeholder="Shortcut"
              />
              <prime_input_text
                class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                v-model="formProgramElement.confidence"
                placeholder="Confidence (0-1)"
              />
            </div>
            <div class="flex items-center gap-4">
              <prime_button
                label="Cancel"
                @click="closeCallback"
                variant="text"
                :disabled="programElementAction.loading.value"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
              <prime_button
                :label="programElementAction.loading.value ? 'جاري الإنشاء…' : 'Create'"
                :loading="programElementAction.loading.value"
                :disabled="programElementAction.loading.value"
                @click="createProgramElement"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
            </div>
          </div>
        </template>
      </prime_dialog>
    </div>

    <div class="card flex justify-center">
      <prime_dialog
        v-model:visible="editProgramElementsVisible"
        pt:root:class="!border-0 !bg-transparent"
        pt:mask:class="backdrop-blur-sm"
      >
        <template #container="{ closeCallback }">
          <div
            class="flex flex-col px-8 py-8 gap-6 rounded-2xl"
            style="
              background-image: radial-gradient(
                circle at left top,
                var(--p-primary-400),
                var(--p-primary-700)
              );
            "
          >
            <div style="margin: auto; font-size: 2rem; font-weight: bolder">
              Edit Program Element
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Name</label>
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.name"
                  placeholder="Element name"
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Description</label>
                <prime_textarea
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formProgramElement.description"
                  placeholder="Description"
                />
              </div>
            </div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Image</label>
                <input type="file" accept="image/*" @change="onImageChangeProgramElement" />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Program</label>
                <select v-model="formProgramElement.program" class="input">
                  <option disabled value="">اختر البرنامج</option>
                  <option v-for="p in programs" :key="p.id" :value="p.id">{{ p.name }}</option>
                </select>
              </div>
            </div>
            <div class="inline-flex flex-col gap-2">
              <label class="text-primary-50 font-semibold">Selector Type</label>
              <select v-model="formProgramElement.selector_type">
                <option disabled value="">Choose</option>
                <option
                  v-for="type in programElementselectorTypes"
                  :key="type.value"
                  :value="type.value"
                >
                  {{ type.label }}
                </option>
              </select>
            </div>
            <div class="inline-flex flex-row gap-2">
              <prime_input_text
                class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                v-model="formProgramElement.x"
                placeholder="X"
              />
              <prime_input_text
                class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                v-model="formProgramElement.y"
                placeholder="Y"
              />
            </div>
            <div class="inline-flex flex-row gap-2">
              <prime_input_text
                class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                v-model="formProgramElement.width"
                placeholder="Width"
              />
              <prime_input_text
                class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                v-model="formProgramElement.height"
                placeholder="Height"
              />
            </div>
            <div class="inline-flex flex-row gap-2">
              <prime_input_text
                class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                v-model="formProgramElement.shortcut"
                placeholder="Shortcut"
              />
              <prime_input_text
                class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                v-model="formProgramElement.confidence"
                placeholder="Confidence"
              />
            </div>
            <div class="flex items-center gap-4">
              <prime_button
                label="Cancel"
                @click="closeCallback"
                variant="text"
                :disabled="programElementAction.loading.value"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
              <prime_button
                :label="programElementAction.loading.value ? 'جاري التحديث…' : 'Update'"
                :loading="programElementAction.loading.value"
                :disabled="programElementAction.loading.value"
                @click="editProgramElement"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
            </div>
          </div>
        </template>
      </prime_dialog>
    </div>

    <div class="card flex justify-center" style="overflow-y: auto">
      <prime_dialog
        v-model:visible="ceateTaskVisible"
        pt:root:class="!border-0 !bg-transparent"
        pt:mask:class="backdrop-blur-sm"
      >
        <template #container="{ closeCallback }">
          <div
            class="flex flex-col px-8 py-8 gap-6 rounded-2xl"
            style="
              background-image: radial-gradient(
                circle at left top,
                var(--p-primary-400),
                var(--p-primary-700)
              );
            "
          >
            <div style="margin: auto; font-size: 2rem; font-weight: bolder">Create Task</div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold"
                  >Task Name <span class="text-red-300">*</span></label
                >
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formTask.name"
                  placeholder="Task Name"
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Description</label>
                <prime_textarea
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formTask.description"
                  placeholder="Description"
                />
              </div>
            </div>
            <div class="inline-flex flex-col gap-2">
              <label class="text-primary-50 font-semibold"
                >Program <span class="text-red-300">*</span></label
              >
              <select v-model="formTask.program" class="input">
                <option disabled value="">اختر البرنامج</option>
                <option v-for="p in programs" :key="p.id" :value="p.id">{{ p.name }}</option>
              </select>
            </div>
            <div class="flex items-center gap-4">
              <prime_button
                label="Cancel"
                @click="closeCallback"
                variant="text"
                :disabled="taskAction.loading.value"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
              <prime_button
                :label="taskAction.loading.value ? 'جاري الإنشاء…' : 'Create'"
                :loading="taskAction.loading.value"
                :disabled="taskAction.loading.value"
                @click="createTask"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
            </div>
          </div>
        </template>
      </prime_dialog>
    </div>

    <div class="card flex justify-center">
      <prime_dialog
        v-model:visible="editTaskVisible"
        pt:root:class="!border-0 !bg-transparent"
        pt:mask:class="backdrop-blur-sm"
      >
        <template #container="{ closeCallback }">
          <div
            class="flex flex-col px-8 py-8 gap-6 rounded-2xl"
            style="
              background-image: radial-gradient(
                circle at left top,
                var(--p-primary-400),
                var(--p-primary-700)
              );
            "
          >
            <div style="margin: auto; font-size: 2rem; font-weight: bolder">Edit Task</div>
            <div class="inline-flex flex-row gap-2">
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Task Name</label>
                <prime_input_text
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formTask.name"
                  placeholder="Task Name"
                />
              </div>
              <div class="inline-flex flex-col gap-2">
                <label class="text-primary-50 font-semibold">Description</label>
                <prime_textarea
                  class="!bg-white/20 !border-0 !p-4 !text-primary-50 w-80"
                  v-model="formTask.description"
                  placeholder="Task description"
                />
              </div>
            </div>
            <div class="inline-flex flex-col gap-2">
              <label class="text-primary-50 font-semibold">Program</label>
              <select v-model="formTask.program" class="input">
                <option disabled value="">اختر البرنامج</option>
                <option v-for="p in programs" :key="p.id" :value="p.id">{{ p.name }}</option>
              </select>
            </div>
            <div class="flex items-center gap-4">
              <prime_button
                label="Cancel"
                @click="closeCallback"
                variant="text"
                :disabled="taskAction.loading.value"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
              <prime_button
                :label="taskAction.loading.value ? 'جاري التحديث…' : 'Update'"
                :loading="taskAction.loading.value"
                :disabled="taskAction.loading.value"
                @click="editTask"
                variant="text"
                class="!p-4 w-full !text-primary-50 !border !border-white/30 hover:!bg-white/10"
              />
            </div>
          </div>
        </template>
      </prime_dialog>
    </div>
  </main>
</template> -->
