# frontend_vue

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```

# 🤖 Automation Dashboard — Project README

---

<div dir="rtl">
  <h2> 🧠 الفكرة الأساسية للمشروع (Project Vision)</h2>
  <p>
  <b>Automation Dashboard</b>
  هو منصة لأتمتة سطح المكتب
  (Desktop Workflow Automation).
  </p>

> تخيل إنك بتبني "وصفة" خطوة بخطوة لجهاز الكمبيوتر:
> **افتح VSCode** → **اضغط Ctrl+Shift+P** → **انتظر 2 ثانية** → **اكتب "build"** → **اضغط Enter**
> الـ Dashboard ده بيخليك تبني الوصفة دي بـ drag & drop — من غير ما تكتب أي كود.

</div>

---

## 🏗️ اللوجيك الكامل (End-to-End Flow)

```
المستخدم
    ↓
يفتح الـ Dashboard في المتصفح
    ↓
يسحب Program أو Element على الـ Canvas (VueFlow)
    ↓
الـ Frontend يبعت للـ Django:
    POST /api/automation/workflow-nodes/   ← ينشئ Node
    POST /api/automation/actions/          ← يربط Action بالـ Node
    ↓
المستخدم يربط الـ Nodes ببعض بـ Edges
    ↓
يضغط "Save Workflow"
    ↓
يضغط "Start Workflow"
    ↓
Django يبعت الـ Workflow للـ Celery Worker
    ↓
الـ Worker ينفذ كل Node بالترتيب:
    - يفتح البرنامج (pyautogui / pywinauto)
    - يضغط الزرار
    - ينتظر
    - يكتب نص
    ↓
النتيجة بترجع للـ Frontend عبر WebSocket
    ↓
LiveConsole يعرض الـ logs في الـ real-time
```

---

## 📦 المكونات الرئيسية (Core Entities)

### 1️⃣ Program (البرنامج)

```
مثال: VSCode, Chrome, Notepad

الـ fields المهمة:
- name:                 "Visual Studio Code"
- executable_path:      "C:/Program Files/VSCode/Code.exe"
- working_directory:    "C:/Users/Hossam/projects"
- window_title_pattern: "VSCode"    ← بنستخدمه عشان نتحقق إن البرنامج فتح
- image:                صورة الـ icon

الـ Django يعمل إيه بيه؟
- بيحفظه في الـ DB
- بيفتحه: subprocess.Popen(executable_path)
- بيشيل فوكس عليه: pywinauto.find_window(window_title_pattern)
```

### 2️⃣ Program Element (عنصر داخل البرنامج)

```
مثال: زرار "Build", input "Search", menu "File"

الـ fields المهمة:
- program:        FK → Program (جوه أنهي برنامج)
- element_type:   "button" | "input" | "menu"
- selector_type:  "image" | "coords" | "text" | "ui"
- selector_value: إزاي نلاقيه (XPath, image path, x/y coords)
- x, y:           إحداثيات الـ element على الشاشة
- confidence:     دقة الـ image matching (0.0 - 1.0)

الـ Django يعمل إيه بيه؟
- selector_type = "image"  → pyautogui.locateOnScreen(image, confidence)
- selector_type = "coords" → pyautogui.click(x, y)
- selector_type = "ui"     → pywinauto.find_element(xpath)
```

### 3️⃣ Workflow (الوصفة)

```
مجموعة Nodes + Edges = تسلسل خطوات تُنفَّذ بالترتيب

الـ fields:
- name, description
- status: "draft" | "active" | "paused"

الـ relations:
- Workflow → [Node1, Node2, Node3]  (nodes)
- Node1 → Node2 → Node3             (edges)
```

### 4️⃣ Workflow Node (خطوة في الـ Workflow)

```
كل Node = خطوة واحدة في الـ automation

الـ fields:
- workflow:    FK → Workflow
- node_type:   "program" | "program-element" | "delay" | "custom"
- label:       اسم يظهر على الـ Canvas
- program:     FK → Program (اختياري)
- element:     FK → ProgramElement (اختياري)
- position_x:  مكانه على الـ Canvas
- position_y:  مكانه على الـ Canvas
- config:      JSON — إعدادات الـ UI (ألوان، أبعاد)

ملاحظة مهمة جداً:
  n.id            = UUID خاص بالـ VueFlow (بيتغير بعد كل save_all)
  n.data.node.backend_id = UUID الحقيقي في الـ Django DB
  → دايماً استخدم backend_id في الـ API calls
```

### 5️⃣ Action (الفعل اللي بيعمله الـ Node)

```
كل Node ليه Action واحدة أو أكتر تُنفَّذ لما تيجي نوبته

أنواع الـ Actions:
┌─────────────────┬──────────────────────────────────────────┐
│  action_type    │  payload                                 │
├─────────────────┼──────────────────────────────────────────┤
│ open_program    │ {}                                       │
│ close_program   │ {}                                       │
│ press           │ { key: "Enter" }                        │
│ hotkey          │ { keys: ["ctrl", "shift", "p"] }        │
│ wait            │ { seconds: 2 }                          │
│ click_element   │ { element_id: "uuid-of-element" }       │
│ type_text       │ { text: "hello world" }                 │
└─────────────────┴──────────────────────────────────────────┘
```

### 6️⃣ Workflow Edge (الربط بين الـ Nodes)

```
بيحدد ترتيب التنفيذ

الـ fields:
- source_node: FK → Node (من أنهي Node)
- target_node: FK → Node (لأنهي Node)
- condition:   "success" | "failure" | "always"

يعني: نفّذ Node2 بس لو Node1 نجح
```

### 7️⃣ Task (قالب جاهز)

```
Task = workflow template مسمّى ومحفوظ
المستخدم يقدر يشيل Task ويحطه على الـ canvas
وكمان يقدر يشغّله مستقلاً
```

---

## 🌐 Django Endpoints — كل Endpoint وهو بيعمل إيه

### Programs

```
GET    /api/automation/programs/              → جيب كل البرامج
POST   /api/automation/programs/              → أنشئ برنامج جديد
GET    /api/automation/programs/{id}/         → جيب برنامج معين
PUT    /api/automation/programs/{id}/         → عدّل برنامج
DELETE /api/automation/programs/{id}/         → احذف برنامج
POST   /api/automation/programs/{id}/open/    → افتح البرنامج على الجهاز
POST   /api/automation/programs/{id}/close/   → اقفل البرنامج
POST   /api/automation/programs/{id}/focus/   → خلّي البرنامج في الـ focus
POST   /api/automation/programs/{id}/maximize/→ كبّر البرنامج
GET    /api/automation/programs/{id}/status/  → هل البرنامج شغّال؟
```

### Program Elements

```
GET    /api/automation/program-elements/       → جيب كل الـ elements
POST   /api/automation/program-elements/       → أنشئ element جديد
GET    /api/automation/program-elements/{id}/  → جيب element معين
PUT    /api/automation/program-elements/{id}/  → عدّل element
DELETE /api/automation/program-elements/{id}/  → احذف element
```

### Workflows

```
GET    /api/automation/workflows/              → جيب كل الـ workflows
POST   /api/automation/workflows/             → أنشئ workflow جديد
GET    /api/automation/workflows/{id}/         → جيب workflow معين
PUT    /api/automation/workflows/{id}/         → عدّل الـ workflow (name, status)
DELETE /api/automation/workflows/{id}/         → احذف الـ workflow
GET    /api/automation/workflows/{id}/full_events/ → جيب الـ nodes + edges كلهم دفعة واحدة
POST   /api/automation/workflows/{id}/save_all/    → احفظ الـ nodes + edges في حركة واحدة
POST   /api/automation/workflows/{id}/run/         → شغّل الـ workflow
```

### Workflow Nodes

```
GET    /api/automation/workflow-nodes/         → جيب كل الـ nodes
POST   /api/automation/workflow-nodes/         → أنشئ node جديد على الـ Canvas
GET    /api/automation/workflow-nodes/{id}/    → جيب node معين
PUT    /api/automation/workflow-nodes/{id}/    → عدّل (position, label, config)
DELETE /api/automation/workflow-nodes/{id}/    → احذف node من الـ Canvas
POST   /api/automation/workflow-nodes/{id}/run/→ شغّل node واحد بس (للاختبار)
```

### Actions

```
GET    /api/automation/actions/                → جيب كل الـ actions
POST   /api/automation/actions/               → أنشئ action جديد وربطه بـ node
GET    /api/automation/actions/{id}/           → جيب action معين
PUT    /api/automation/actions/{id}/           → عدّل نوع الـ action أو الـ payload
DELETE /api/automation/actions/{id}/           → احذف action
```

### Workflow Edges

```
GET    /api/automation/workflow-edges/         → جيب كل الـ edges
POST   /api/automation/workflow-edges/         → ربط node بـ node تاني
DELETE /api/automation/workflow-edges/{id}/    → افصل الـ nodes
```

### Tasks

```
GET    /api/automation/tasks/                  → جيب كل الـ tasks
POST   /api/automation/tasks/                  → أنشئ task template
GET    /api/automation/tasks/{id}/             → جيب task معين
PUT    /api/automation/tasks/{id}/             → عدّل task
DELETE /api/automation/tasks/{id}/             → احذف task
```

---

## 🔌 Plugin System — الفكرة

```

كل Action type = Plugin مستقل:

plugins/
├── PluginRegistry.js ← سجل كل الـ plugins
├── PluginSDK.js ← الـ interface المشترك
└── builtin/
├── OpenProgramPlugin.js → ينفذ: subprocess.run(executable_path)
├── ClickElementPlugin.js → ينفذ: pyautogui.click(x, y)
├── WaitPlugin.js → ينفذ: time.sleep(seconds)
└── AIActionPlugin.js → ينفذ: OpenAI API call

الفكرة: المستخدم يقدر يضيف Plugin جديد بدون ما يغير أي كود قديم

```

---

## 🗺️ NodeMarketplace — الفكرة

```
NodeMarketplace.vue = متجر الـ Nodes

المستخدم يشوف:
┌─────────────────────────────────────┐
│  🖥️ Open Program     [add to canvas] │
│  🖱️ Click Element    [add to canvas] │
│  ⏳ Wait             [add to canvas] │
│  🤖 AI Action        [add to canvas] │
│  📧 Send Email       [add to canvas] │ ← من مجتمع خارجي
│  📊 Excel Export     [add to canvas] │ ← plugin مخصص
└─────────────────────────────────────┘

كل بطاقة = NodePluginCard.vue
```

---

## 📁 Project Structure (المشروع الكامل)

```
src/
├── stores/                          ← 💾 البيانات والـ API calls
│   ├── useWorkflowStore.js          workflows, nodes, edges, save, autoLayout
│   ├── useProgramStore.js           programs, form, CRUD, open/close/focus
│   ├── useProgramElementStore.js    elements, form, CRUD
│   └── useTaskStore.js              tasks, form, CRUD, runId
│
├── composables/                     ← 🔧 Logic مشترك
│   ├── useAsyncAction.js            UX engine: loading + toast + validate
│   ├── useApiTracker.js             تتبع كل API call → ApiFlowPanel
│   └── useNodeDragDrop.js           drag/drop logic للـ canvas
│
├── services/                        ← 🌐 كل الـ HTTP calls
│   ├── AutomationService.js         كل endpoints
│   └── WorkerService.js             WebSocket للـ real-time execution
│
├── plugins/                         ← 🔌 نظام الـ Plugins
│   ├── PluginSDK.js                 definePlugin() — contract لكل plugin
│   ├── PluginRegistry.js            singleton: register/get/buildPayload
│   └── builtin/
│       ├── OpenProgramPlugin.js     open_program → subprocess.Popen()
│       ├── ClickElementPlugin.js    click_element → pyautogui.click()
│       ├── WaitPlugin.js            wait → time.sleep()
│       └── AIActionPlugin.js        ai_action → OpenAI Vision API
│
├── views/
│   └── AutomationView.vue           🎨 المتحكم الرئيسي — UI state فقط
│
└── components/Automation/
    ├── Action/
    │   ├── ActionPanel.vue
    ├── Edge/
    │   ├── CustomEdge.vue
    └── Execution/
        ├── LiveConsole.vue          WebSocket log console — fixed bottom bar
        └── RealtimeGraph.vue        Bar chart: execution time per node
    ├── Node/
    │   ├── NodeMarketplace.vue      Sidebar: Programs + Elements + Plugins tabs
    │   ├── NodeVisualBuilder.vue    Configure node before adding to canvas
    │   └── NodePluginCard.vue       بطاقة plugin واحدة — draggable
    ├── Program/
    │   ├── CreateProgram.vue        Dialog إنشاء برنامج
    │   └── EditProgram.vue          Dialog تعديل برنامج
    ├── ProgramElement/
    │   ├── CreateProgramElement.vue        Dialog إنشاء برنامج
    │   └── EditProgramElement.vue          Dialog تعديل برنامج
    ├── Workflow/
    │   ├── WorkflowCanvas.vue       VueFlow wrapper — props/emits فقط, لا API
    │   ├── WorkflowToolbar.vue      Save/Run/Layout/Status buttons
    │   └── WorkflowVersions.vue     Version history drawer (Phase 3)


```

---

---

## 🔗 كيف ترتبط الـ Components ببعض

```
AutomationView.vue  (المتحكم الرئيسي — stores + logic)
│
├── <NodeMarketplace>        ← الـ sidebar
│     @drag-start            → startDrag({ type, id })
│     @create-program        → createProgramVisible = true
│     @select-workflow       → selectWorkflow(id)
│
├── <WorkflowCanvas>         ← VueFlow wrapper
│     :nodes :edges
│     @node-click            → onNodeSelect()
│     @connect               → onConnect()
│     @drop                  → onDrop() → createNode()
│     @node-drag-stop        → enqueueUpdate()
│     ↳ slot#toolbar:
│         <WorkflowToolbar>
│               @save        → saveWorkflow()
│               @run         → startWorkflow()
│               @auto-layout → autoLayout(dir)
│               @update-status → updateStatusWorkflow()
│
├── <ActionPanel>            ← يظهر عند اختيار node
│     @create-action         → createNodeAction()
│     @update-action         → updateNodeAction()
│     @delete-action         → deleteNodeAction()
│
├── <LiveConsole>            ← fixed bottom — يظهر عند تشغيل workflow
│     :task-run-id
│     WebSocket → ws://localhost:8000/ws/workflow/{taskRunId}/
│     Message format: { type: 'log'|'status'|'done', level, message, node_id }
│
├── <RealtimeGraph>          ← Dialog metrics أثناء التنفيذ
│     :nodes :task-run-id
│     WebSocket نفس الـ LiveConsole — بس بيرسم charts
│
└── <WorkflowVersions>       ← Drawer يمين
      :workflow-id
      @restore               → loadWorkflowEvents(id)
```

---

---

## 🔧 Composables — التفاصيل

### `useAsyncAction.js` — UX Engine

```
كل API call في المشروع بيمر عبره.

run(apiFn, options):
  ↓ validate()          → يتحقق من الـ form
  ↓ tracker.execute()   → يظهر في ApiFlowPanel
  ↓ onSuccess(result)   → business logic (غلق dialog، update state)
  ↓ onError(err)        → rollback لو محتاج
  ↓ toast               → رسالة للمستخدم

الـ loading state:
  programAction.loading → :disabled="programAction.loading" على الـ button
```

### `useToastHelper.js` — Toast Wrapper

```
success('تم', 'البيانات محفوظة')
error('خطأ', 'تفاصيل الخطأ')
warn('تنبيه', 'تحقق من البيانات')
apiError(err, 'اسم العملية')   ← الأهم — بيقرأ Django errors تلقائياً

مثال Django 400:
  { name: ["هذا الحقل مطلوب"] }
  → يعرض: "name: هذا الحقل مطلوب"
```

### `useNodeDragDrop.js` — Canvas Drag & Drop

```
startDrag(item)      ← من الـ sidebar
onDragOver(e)        ← على الـ canvas
onDrop(e)            ← يكلم الـ backend وينشئ node
onNodeDragStop(node) ← يحفظ الـ position بعد الـ drag (debounced)

المهم:
  onNodeDragStop → bypass tracker (مش في ApiFlowPanel)
  → debounced 300ms + queue + deduplication
```

### `usePrograms.js` — Programs UI Logic

```
بيجمع كل اللوجيك الخاص بالـ Programs من ناحية الـ View:
  - dialog visibility (createProgramVisible, editProgramVisible)
  - create / edit / delete + confirm dialogs
  - open / close / focus / maximize

الـ split:
  useProgramStore → API + data + validation
  usePrograms     → dialog state + toast + confirm
```

