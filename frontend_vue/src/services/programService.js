// import api from './api'
// export default {
//   list() { return api.get('/programs/') },
//   open(id) { return api.get(`/programs/${id}/open/`) },
//   create(data) { return api.post('/programs/', data) },
//   update(id, data) { return api.put(`/programs/${id}/`, data) }
// }
import api from './api'

export default {
  // Get all programs
  getPrograms() {
    return api.get('automation/programs/')
  },

  // Create new program
  createProgram(data) {
    return api.post('automation/programs/', data)
  },

  // open program (runs executable)
  openProgram(id) {
    return api.get(`automation/programs/${id}/open/`)
  },
}
