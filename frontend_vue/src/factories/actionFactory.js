export function buildActionsFromNode(node) {
  const actions = []

  const nodeType = node.node_type
  const backendNodeId = node.backend_id

  // 1️⃣ PROGRAM
  if (nodeType === 'program') {
    actions.push({
      action_type: 'open_program',
      node: backendNodeId,
      payload: {
        program_id: node.program,
      },
    })
  }

  // 2️⃣ PROGRAM ELEMENT
  if (nodeType === 'program-element') {
    actions.push({
      action_type: 'element_click',
      node: backendNodeId,
      payload: {
        element_id: node.element,
      },
    })
  }

  // 3️⃣ DELAY
  if (nodeType === 'delay') {
    actions.push({
      action_type: 'delay',
      node: backendNodeId,
      payload: {
        seconds: node.config?.seconds || 1,
      },
    })
  }

  return actions
}
