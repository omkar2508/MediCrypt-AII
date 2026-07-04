import axios from './axiosClient'

type LoginDto = { email: string; password: string }

export async function login(credentials: LoginDto) {
  const res = await axios.post('/auth/login', credentials)
  const token = res.data?.access_token || res.data?.token
  if (token) localStorage.setItem('medicrypt_token', token)
  return res.data
}

export function logout() {
  localStorage.removeItem('medicrypt_token')
}

export function getToken(): string | null {
  return localStorage.getItem('medicrypt_token')
}

export async function me() {
  const res = await axios.get('/auth/me')
  return res.data
}
