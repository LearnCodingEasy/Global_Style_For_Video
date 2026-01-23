<!-- <template>
  <div class="about">
    <div class="flex flex-col min-h-screen">
      <header
        class="sticky top-0 z-10 bg-background-light/80 dark:bg-background-dark/80 backdrop-blur-sm"
      >
        <div
          class="flex items-center justify-between p-4 border-b border-primary/20 dark:border-primary/30"
        >
          <h1
            class="flex-1 text-xl font-bold text-center text-background-dark dark:text-background-light"
          >
            Koshari Shop
          </h1>
          <button class="p-2 text-background-dark dark:text-background-light">
            <svg
              fill="currentColor"
              height="24"
              viewBox="0 0 256 256"
              width="24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M222.14,58.87A8,8,0,0,0,216,56H54.68L49.79,29.14A16,16,0,0,0,34.05,16H16a8,8,0,0,0,0,16h18L59.56,172.29a24,24,0,0,0,5.33,11.27,28,28,0,1,0,44.4,8.44h45.42A27.75,27.75,0,0,0,152,204a28,28,0,1,0,28-28H83.17a8,8,0,0,1-7.87-6.57L72.13,152h116a24,24,0,0,0,23.61-19.71l12.16-66.86A8,8,0,0,0,222.14,58.87ZM96,204a12,12,0,1,1-12-12A12,12,0,0,1,96,204Zm96,0a12,12,0,1,1-12-12A12,12,0,0,1,192,204Zm4-74.57A8,8,0,0,1,188.1,136H69.22L57.59,72H206.41Z"
              ></path>
            </svg>
          </button>
        </div>
        <nav class="flex justify-around px-4 border-b border-primary/20 dark:border-primary/30">
          <a class="py-3 text-sm font-bold border-b-2 text-primary border-primary" href="#">Home</a>
          <a
            class="py-3 text-sm font-bold text-background-dark/60 dark:text-background-light/60 border-b-2 border-transparent hover:text-primary hover:border-primary"
            href="#"
            >Menu</a
          >
          <a
            class="py-3 text-sm font-bold text-background-dark/60 dark:text-background-light/60 border-b-2 border-transparent hover:text-primary hover:border-primary"
            href="#"
            >Offers</a
          >
          <a
            class="py-3 text-sm font-bold text-background-dark/60 dark:text-background-light/60 border-b-2 border-transparent hover:text-primary hover:border-primary"
            href="#"
            >Contact</a
          >
        </nav>
      </header>
      <main class="flex-grow">
        <section class="p-4">
          <h2
            class="px-4 pt-4 pb-4 text-2xl font-bold text-background-dark dark:text-background-light"
          >
            Our Menu
          </h2>
          <div class="space-y-6">
            <div class="flex gap-4 p-4 rounded-lg bg-primary/10 dark:bg-primary/20">
              <div class="flex-1">
                <p class="text-xs font-bold uppercase text-primary">Popular</p>
                <h3 class="text-lg font-bold text-background-dark dark:text-background-light">
                  Koshari
                </h3>
                <p class="mt-1 text-sm text-background-dark/70 dark:text-background-light/70">
                  A traditional Egyptian dish with rice, lentils, pasta, chickpeas, and a spicy
                  tomato sauce.
                </p>
                <p class="mt-4 text-lg font-bold text-primary">$5.99</p>
              </div>
              <div class="w-24 h-24 overflow-hidden rounded-lg">
                <img
                  alt="Koshari"
                  class="object-cover w-full h-full"
                  src="https://lh3.googleusercontent.com/aida-public/AB6AXuCi0mXuBpwAQH4DzqExO4lkLFbLZMT94bjgg-VP2pqtEJKSVzQq0HdDyoBeVGFJgqYyMdn4XngrrJYuglyF2vFn2ERWhJSOi8K4_i3M2Mq7A6vK5ARh8nQl0_-_BCy9AbrUwspVqFGFvFsVnyqHP-p44BiXxjI2emVUxqrNdKZsddsfIWjuZYNz8fO3nVrCFuMeYLp-U-57W5Drd608_rmKud5qeBPiwICTsMlvp7icmpJSo2hHFOclzQCmhnmkXrRmbgalFGFR2Rw"
                />
              </div>
            </div>
            <div class="flex gap-4 p-4 rounded-lg bg-primary/10 dark:bg-primary/20">
              <div class="flex-1">
                <p class="text-xs font-bold uppercase text-primary">Popular</p>
                <h3 class="text-lg font-bold text-background-dark dark:text-background-light">
                  Foul Medames
                </h3>
                <p class="mt-1 text-sm text-background-dark/70 dark:text-background-light/70">
                  Stewed fava beans served with olive oil, lemon juice, and spices.
                </p>
                <p class="mt-4 text-lg font-bold text-primary">$4.49</p>
              </div>
              <div class="w-24 h-24 overflow-hidden rounded-lg">
                <img
                  alt="Foul Medames"
                  class="object-cover w-full h-full"
                  src="https://lh3.googleusercontent.com/aida-public/AB6AXuC7XsZL_hLwY-iE7jl7oB_yZZEn-gtG9Snumf5NM5A9BRFDp50YgMW1oUtd2rqN5J3FkyB2rKZ76712YQOEdTuCsn_nyAU3I07TDnAqj6K3SgmX7DPKP0FXoAX26M3k0ku1wYZSVePec2qXSATNKuP5_lY4SXCanrEmBiIbRw2YXw2V0g0ohPHVHD1Z4dM6y00c4upFLFbEVOT-Wj0wmSsLaDKROtA2LCF-VhnrN1RKc5XpYhY-Kjyc2gsm9Em3KOLyMiDyNq8Ylis"
                />
              </div>
            </div>
            <div class="flex gap-4 p-4 rounded-lg bg-primary/10 dark:bg-primary/20">
              <div class="flex-1">
                <p class="text-xs font-bold uppercase text-primary">Popular</p>
                <h3 class="text-lg font-bold text-background-dark dark:text-background-light">
                  Falafel
                </h3>
                <p class="mt-1 text-sm text-background-dark/70 dark:text-background-light/70">
                  Deep-fried patties made from ground chickpeas or fava beans, often served in pita
                  bread.
                </p>
                <p class="mt-4 text-lg font-bold text-primary">$3.99</p>
              </div>
              <div class="w-24 h-24 overflow-hidden rounded-lg">
                <img
                  alt="Falafel"
                  class="object-cover w-full h-full"
                  src="https://lh3.googleusercontent.com/aida-public/AB6AXuDREkO8N8cp63YBH8WzNcBZCt2quy_AFmlJZo2b3WOEJN4eUHnoDdhrbLA4C34D0g5lwZSpLyL7asf3I5qRbRoUFzxeQ_Jbnfpgy-dQxn9rO0CB_Mxlt1mpFwh8w0qftJWrfX_SLH3TCXWc7Uc4kCwDE38-fUQDDfEwoD9rAiXJ6AGWkvrbgnaMPCbvJy6EOzO5nNLInxvl79U_jjVARwS74L4jmI3gYBW7rFNsqHJTTmEr4hwbSJS8cSsxHkRdZG_SFqK9jRB2q3A"
                />
              </div>
            </div>
          </div>
        </section>
        <section class="p-4">
          <h2
            class="px-4 pt-4 pb-4 text-2xl font-bold text-background-dark dark:text-background-light"
          >
            Toppings
          </h2>
          <div class="grid grid-cols-2 gap-4">
            <div class="p-4 rounded-lg bg-primary/10 dark:bg-primary/20">
              <img
                alt="Spicy Sauce"
                class="object-cover w-full h-24 rounded"
                src="https://lh3.googleusercontent.com/aida-public/AB6AXuBcfdBV6LGCF3J-Lj3ZrhwAzgixoL1RVQq8rzq0UfKy4hhumkvmfrQ9l86N8PRZfnnj89bZQ6XWndtcnLOcZhv9HqPx9IOoTGNwzRlkruuvShcpTG0MTnwI6djRXLDgx26QzRdrDlvfV3yjCKj-WEido0bwefhL3xGogC8nnlQMcVDd2hiZ6whl6dD36brvhmXtF6TcURAIPuavHBLQyUL-kN6WTm8xCrZewXph1R8zDlQVz275ORs81G4CTaEOvYolkZMdVQnsacA"
              />
              <h3 class="mt-2 font-bold text-background-dark dark:text-background-light">
                Spicy Sauce
              </h3>
              <p class="mt-1 text-xs text-background-dark/70 dark:text-background-light/70">
                A fiery tomato-based sauce.
              </p>
              <p class="mt-2 font-bold text-primary">$0.99</p>
            </div>
            <div class="p-4 rounded-lg bg-primary/10 dark:bg-primary/20">
              <img
                alt="Vinegar Garlic Sauce"
                class="object-cover w-full h-24 rounded"
                src="https://lh3.googleusercontent.com/aida-public/AB6AXuAJeIZYDPyHDO2lT4nA-rvc2XDLwvV51BXVanIK9VDVrtCuEeq6vNil6iVhP2W8y8h9l8OFQokLHOujBmB_l8djXoYjNXpsltcDJKRndwWZoe-yDxFG3Tc3pkurKCMy5tq-7HYyI5jrHkHZnk2OQ-zontBr1N0jgTY_jUZuXNTlO2ZKsdu1gv8zzs-gS55oMPy1lm3Jc8oZgCg7c-6y7DSIN84hsawDdQnYqM7X1UB-XBftWNwJJFkY9o73XVSNCoaXew87PrMwtqM"
              />
              <h3 class="mt-2 font-bold text-background-dark dark:text-background-light">
                Vinegar Garlic Sauce
              </h3>
              <p class="mt-1 text-xs text-background-dark/70 dark:text-background-light/70">
                A tangy sauce with vinegar and garlic.
              </p>
              <p class="mt-2 font-bold text-primary">$0.79</p>
            </div>
            <div class="p-4 rounded-lg bg-primary/10 dark:bg-primary/20">
              <img
                alt="Crispy Onions"
                class="object-cover w-full h-24 rounded"
                src="https://lh3.googleusercontent.com/aida-public/AB6AXuAKERQLwzSMwt3e3FdjL30y_eOgBP0BCt3wxuJjRCKDtB6O8rNcChua8C1EFvcSk6YHZXrdRTrFN89tRAnJf22J2kbH4WnfUj95qihAeMHVtdC1AlHiRhMNg8hvZKfZQwhiUVz64rj-UiiRKX2Z3iwCO6FLgG5dSuAdGDrhN_fjmiwnDhSOaOqbv4F-KO91UEgEFkO0DUZzG6ziIlo-BC7_ghv4EgJgR6nR8u0hInWOy5hLtmEMPKS2Kix5VOwpPx0X7E3oLpwGkdo"
              />
              <h3 class="mt-2 font-bold text-background-dark dark:text-background-light">
                Crispy Onions
              </h3>
              <p class="mt-1 text-xs text-background-dark/70 dark:text-background-light/70">
                Fried onions for a delightful crunch.
              </p>
              <p class="mt-2 font-bold text-primary">$0.59</p>
            </div>
          </div>
        </section>
      </main>
      <footer
        class="sticky bottom-0 bg-background-light dark:bg-background-dark border-t border-primary/20 dark:border-primary/30"
      >
        <nav class="flex justify-around py-2">
          <a class="flex flex-col items-center gap-1 text-primary" href="#">
            <svg
              fill="currentColor"
              height="24"
              viewBox="0 0 256 256"
              width="24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M224,115.55V208a16,16,0,0,1-16,16H168a16,16,0,0,1-16-16V168a8,8,0,0,0-8-8H112a8,8,0,0,0-8,8v40a16,16,0,0,1-16,16H48a16,16,0,0,1-16-16V115.55a16,16,0,0,1,5.17-11.78l80-75.48.11-.11a16,16,0,0,1,21.53,0,1.14,1.14,0,0,0,.11.11l80,75.48A16,16,0,0,1,224,115.55Z"
              ></path>
            </svg>
            <span class="text-xs font-medium">Home</span>
          </a>
          <a
            class="flex flex-col items-center gap-1 text-background-dark/60 dark:text-background-light/60 hover:text-primary"
            href="#"
          >
            <svg
              fill="currentColor"
              height="24"
              viewBox="0 0 256 256"
              width="24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M224,128a8,8,0,0,1-8,8H40a8,8,0,0,1,0-16H216A8,8,0,0,1,224,128ZM40,72H216a8,8,0,0,0,0-16H40a8,8,0,0,0,0,16ZM216,184H40a8,8,0,0,0,0,16H216a8,8,0,0,0,0-16Z"
              ></path>
            </svg>
            <span class="text-xs font-medium">Menu</span>
          </a>
          <a
            class="flex flex-col items-center gap-1 text-background-dark/60 dark:text-background-light/60 hover:text-primary"
            href="#"
          >
            <svg
              fill="currentColor"
              height="24"
              viewBox="0 0 256 256"
              width="24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M205.66,61.64l-144,144a8,8,0,0,1-11.32-11.32l144-144a8,8,0,0,1,11.32,11.31ZM50.54,101.44a36,36,0,0,1,50.92-50.91h0a36,36,0,0,1-50.92,50.91ZM56,76A20,20,0,1,0,90.14,61.84h0A20,20,0,0,0,56,76ZM216,180a36,36,0,1,1-10.54-25.46h0A35.76,35.76,0,0,1,216,180Zm-16,0a20,20,0,1,0-5.86,14.14A19.87,19.87,0,0,0,200,180Z"
              ></path>
            </svg>
            <span class="text-xs font-medium">Offers</span>
          </a>
          <a
            class="flex flex-col items-center gap-1 text-background-dark/60 dark:text-background-light/60 hover:text-primary"
            href="#"
          >
            <svg
              fill="currentColor"
              height="24"
              viewBox="0 0 256 256"
              width="24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M222.37,158.46l-47.11-21.11-.13-.06a16,16,0,0,0-15.17,1.4,8.12,8.12,0,0,0-.75.56L134.87,160c-15.42-7.49-31.34-23.29-38.83-38.51l20.78-24.71c.2-.25.39-.5.57-.77a16,16,0,0,0,1.32-15.06l0-.12L97.54,33.64a16,16,0,0,0-16.62-9.52A56.26,56.26,0,0,0,32,80c0,79.4,64.6,144,144,144a56.26,56.26,0,0,0,55.88-48.92A16,16,0,0,0,222.37,158.46ZM176,208A128.14,128.14,0,0,1,48,80,40.2,40.2,0,0,1,82.87,40a.61.61,0,0,0,0,.12l21,47L83.2,111.86a6.13,6.13,0,0,0-.57.77,16,16,0,0,0-1,15.7c9.06,18.53,27.73,37.06,46.46,46.11a16,16,0,0,0,15.75-1.14,8.44,8.44,0,0,0,.74-.56L168.89,152l47,21.05h0s.08,0,.11,0A40.21,40.21,0,0,1,176,208Z"
              ></path>
            </svg>
            <span class="text-xs font-medium">Contact</span>
          </a>
        </nav>
      </footer>
    </div>
  </div>
</template>

<style></style> -->

<script>
export default { name: 'AboutView' }
</script>
<script setup>
// 1
// استيراد المكتبات
import { ref } from 'vue'
// 🔍 وإدارة الحالة Vue Flow تكامل
import { VueFlow } from '@vue-flow/core'
import { Panel } from '@vue-flow/core'
import { useVueFlow } from '@vue-flow/core'
// 🖼️ Vue Flow إضافة خلفية لمخططات
import { Background } from '@vue-flow/background'
// 🎛️ عناصر تحكم لتحكم في حالة المخطط
import { Controls } from '@vue-flow/controls'
// 🌍 خريطة مصغرة لرؤية مخطط التطبيق
import { MiniMap } from '@vue-flow/minimap'
// 📦 أدوات سحب وإفلات لواجهة المستخدم
import vuedraggable from 'vuedraggable'

//
//
//
//
//
const currentWorkflowName = ref('VueFlow workspace')

const updateVueFlow = () => {
  currentWorkflowName.value = 'Workflow Name'
}
console.log('updateVueFlow: ', updateVueFlow)

const nodes = ref([
  { id: '1', position: { x: 10, y: 80 }, data: { label: 'Start' } },
  { id: '2', position: { x: 15, y: 200 }, data: { label: 'End' } },
])
const edges = ref([{ id: 'e1-2', source: '1', target: '2' }])
// 2
function onNodeClick(e) {
  console.log('Node Click:', e.node)
}

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
