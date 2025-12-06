// src/services/workflowService.js
import api from './api'

const workflowService = {
  list() {
    return api.get('/automation/workflows/')
  },

  get(id) {
    return api.get(`/automation/workflows/${id}/`)
  },

  create(data) {
    return api.post('/automation/workflows/', data)
  },

  update(id, data) {
    return api.put(`/automation/workflows/${id}/`, data)
  },

  delete(id) {
    return api.delete(`/automation/workflows/${id}/`)
  },

  getTasks(id) {
    return api.get(`/automation/workflows/${id}/tasks/`)
  },

  saveLayout(payload) {
    return api.post('/automation/workflows/save-layout/', payload)
  },
}

export default workflowService
