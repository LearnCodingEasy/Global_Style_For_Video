// edgeFactory.js

export function createEdge(source, target) {
  return {
    id: `edge-${source}-${target}`,
    source,
    target,
    type: 'custom',
  }
}
