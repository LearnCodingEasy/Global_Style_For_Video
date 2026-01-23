// edgeFactory.js

export const createEdge = ({ source, target }) => ({
  id: `temp-${Date.now()}`,
  source,
  target,
  type: 'custom',
  data: {},
})
