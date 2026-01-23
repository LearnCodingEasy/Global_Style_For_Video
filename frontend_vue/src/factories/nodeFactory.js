// factories/nodeFactory.js

import api from '@/services/AutomationService'

export const createProgramNode = (programId, position) => ({
  id: `${programId}`,
  type: 'custom',
  position,
  data: {
    label: 'Program Node',
    programId,
    runTask: async () => {
      try {
        await api.openProgram(programId)
        alert('Program Opened!')
      } catch (err) {
        console.error('Failed to open program:', err)
      }
    },
  },
})

export const createTaskNode = (taskTemplate, position) => ({
  id: `temp-${Date.now()}`,
  type: 'custom',
  position,
  data: {
    label: taskTemplate.name,
    task: taskTemplate,
    runTask: async () => {
      try {
        await api.createAction({
          action_type: taskTemplate.action_type,
          payload: taskTemplate.payload || {},
        })
        alert(`Task ${taskTemplate.name} executed!`)
      } catch (err) {
        console.error('Failed to execute task:', err)
      }
    },
  },
})

export const createWorkflowNode = (type, position) => ({
  id: `temp-${Date.now()}`,
  type: 'custom',
  position,
  data: { label: type },
})
