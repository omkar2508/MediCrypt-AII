export type StoredKey = {
  key_id: string
  created_at: string
  secret_b64: string
}

const STORAGE_KEY = 'medicrypt_keys_v1'

function loadStore(): Record<string, StoredKey> {
  const raw = localStorage.getItem(STORAGE_KEY)
  if (!raw) return {}
  try {
    return JSON.parse(raw)
  } catch (e) {
    return {}
  }
}

function saveStore(store: Record<string, StoredKey>) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(store))
}

function bytesToBase64(bytes: Uint8Array) {
  let binary = ''
  const len = bytes.byteLength
  for (let i = 0; i < len; i++) binary += String.fromCharCode(bytes[i])
  return btoa(binary)
}

function base64ToBytes(b64: string) {
  const binary = atob(b64)
  const len = binary.length
  const bytes = new Uint8Array(len)
  for (let i = 0; i < len; i++) bytes[i] = binary.charCodeAt(i)
  return bytes
}

export function listKeys() {
  const store = loadStore()
  return Object.values(store).map((k) => ({ key_id: k.key_id, created_at: k.created_at }))
}

export function createKey() {
  const id = (crypto as any).randomUUID ? (crypto as any).randomUUID() : Math.random().toString(36).slice(2)
  const secret = new Uint8Array(32)
  crypto.getRandomValues(secret)
  const secret_b64 = bytesToBase64(secret)
  const entry: StoredKey = { key_id: id, created_at: new Date().toISOString(), secret_b64 }
  const store = loadStore()
  store[id] = entry
  saveStore(store)
  return { key_id: id, created_at: entry.created_at }
}

export function deleteKey(key_id: string) {
  const store = loadStore()
  delete store[key_id]
  saveStore(store)
}

export function getSecretBytes(key_id: string): Uint8Array | null {
  const store = loadStore()
  const entry = store[key_id]
  if (!entry) return null
  return base64ToBytes(entry.secret_b64)
}

export async function exportEvaluationKey(key_id: string) {
  const secret = getSecretBytes(key_id)
  if (!secret) throw new Error('key not found')
  const hash = await crypto.subtle.digest('SHA-256', secret)
  const hBytes = new Uint8Array(hash)
  return bytesToBase64(hBytes)
}

export function exportSecretForBackup(key_id: string) {
  const store = loadStore()
  const entry = store[key_id]
  if (!entry) throw new Error('key not found')
  return entry.secret_b64
}
