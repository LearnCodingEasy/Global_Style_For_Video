<template>
  <div class="card">
    <prime_stepper value="1">
      <prime_step_item value="1">
        <prime_step>Header I</prime_step>
        <prime_step_panels v-slot="{ activateCallback }">
          <div class="flex flex-col h-48">
            <div
              class="border-2 border-dashed border-surface-200 dark:border-surface-700 rounded bg-surface-50 dark:bg-surface-950 flex-auto flex justify-center items-center font-medium"
            >
              Content I
            </div>
          </div>
          <div class="py-6">
            <prime_button label="Next" @click="activateCallback('2')" />
          </div>
        </prime_step_panels>
      </prime_step_item>
      <prime_step_item value="2">
        <prime_step>Header II</prime_step>
        <prime_step_panels v-slot="{ activateCallback }">
          <div class="flex flex-col h-48">
            <div
              class="border-2 border-dashed border-surface-200 dark:border-surface-700 rounded bg-surface-50 dark:bg-surface-950 flex-auto flex justify-center items-center font-medium"
            >
              Content II
            </div>
          </div>
          <div class="flex py-6 gap-2">
            <prime_button label="Back" severity="secondary" @click="activateCallback('1')" />
            <prime_button label="Next" @click="activateCallback('3')" />
          </div>
        </prime_step_panels>
      </prime_step_item>
      <prime_step_item value="3">
        <prime_step>Header III</prime_step>
        <prime_step_panels v-slot="{ activateCallback }">
          <div class="flex flex-col h-48">
            <div
              class="border-2 border-dashed border-surface-200 dark:border-surface-700 rounded bg-surface-50 dark:bg-surface-950 flex-auto flex justify-center items-center font-medium"
            >
              Content III
            </div>
          </div>
          <div class="py-6">
            <prime_button label="Back" severity="secondary" @click="activateCallback('2')" />
          </div>
        </prime_step_panels>
      </prime_step_item>
    </prime_stepper>
  </div>
</template>

<script>
export default { name: 'AutomationView' }
</script>

<style lang="scss" scoped></style>
