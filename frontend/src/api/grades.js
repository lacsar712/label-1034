import request from './request'

export function getGrades(params) {
  return request.get('/grades', { params })
}

export function getGrade(id) {
  return request.get(`/grades/${id}`)
}

export function createGrade(data) {
  return request.post('/grades', data)
}

export function updateGrade(id, data) {
  return request.put(`/grades/${id}`, data)
}

export function deleteGrade(id) {
  return request.delete(`/grades/${id}`)
}
