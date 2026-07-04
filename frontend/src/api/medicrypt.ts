import axios from './axiosClient'

export type CiphertextEnvelope = {
  key_id: string
  ciphertext: number[]
  metadata?: Record<string, unknown>
}

export async function uploadEncryptedRecord(payload: CiphertextEnvelope) {
  const res = await axios.post('/records/encrypted', payload)
  return res.data
}

export async function getPrediction(recordId: string) {
  const res = await axios.get(`/predictions/${recordId}`)
  return res.data
}

export async function listRecords() {
  const res = await axios.get('/records')
  return res.data
}

export async function registerEvaluationKey(key_id: string, evalKeyB64: string) {
  // convert base64 string into number[] payload (bytes)
  const binary = atob(evalKeyB64)
  const arr: number[] = []
  for (let i = 0; i < binary.length; i++) arr.push(binary.charCodeAt(i))
  const body = { key_id, payload: arr }
  const res = await axios.post('/encryption/register-key', body)
  return res.data
}

export async function getRegisteredKeys() {
  const res = await axios.get('/encryption/keys')
  return res.data
}
