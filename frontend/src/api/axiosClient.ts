import axios from 'axios'

const API_BASE = (import.meta.env.VITE_API_BASE as string) || '/api'

const axiosInstance = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
})

axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem('medicrypt_token')
  if (token) {
    if (!config.headers) config.headers = {}
    ;(config.headers as Record<string, string>)['Authorization'] = `Bearer ${token}`
  }
  return config
})

export default axiosInstance
