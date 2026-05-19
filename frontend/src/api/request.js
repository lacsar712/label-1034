import axios from 'axios'
import { ElMessage } from 'element-plus'

const baseURL = (typeof window !== 'undefined' && window.__BASE_URL__) ? window.__BASE_URL__ : '/api'

export const request = axios.create({
  baseURL,
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
})

request.interceptors.response.use(
  (res) => res.data,
  (err) => {
    const msg = err.response?.data?.detail || err.message || '请求失败'
    if (typeof msg === 'string') {
      ElMessage.error(msg)
    } else if (Array.isArray(msg)) {
      ElMessage.error(msg.map((m) => m.msg || JSON.stringify(m)).join('；'))
    } else {
      ElMessage.error(JSON.stringify(msg))
    }
    return Promise.reject(err)
  }
)

export default request
