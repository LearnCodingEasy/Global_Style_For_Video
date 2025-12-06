import api from './api'
export default {
  list() {
    return api.get('/automation/tasks/')
  },
  detail(id) {
    return api.get(`/automation/tasks/${id}/`)
  },
  create(payload) {
    return api.post('/automation/tasks/', payload)
  },
  update(id, payload) {
    return api.put(`/automation/tasks/${id}/`, payload)
  },
  run(id) {
    return api.post(`/automation/tasks/${id}/run/`)
  },
}
