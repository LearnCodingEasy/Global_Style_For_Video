// nodeFactory.js

export function createProgramNode(program, position) {
  return {
    id: `program-${program.id}`,
    type: 'custom',
    position,
    data: {
      label: program.name,
      type: 'program',
      programId: program.id,
    },
  }
}

export function createTaskNode(task, position) {
  return {
    id: `task-${task.id}`,
    type: 'custom',
    position,
    data: {
      label: task.name,
      type: 'task',
      taskId: task.id,
    },
  }
}

export function createWorkflowNode(workflow, position) {
  return {
    id: `workflow-${workflow.id}`,
    type: 'custom',
    position,
    data: {
      label: workflow.name,
      type: 'workflow',
      workflowId: workflow.id,
    },
  }
}
