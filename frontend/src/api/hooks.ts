import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import * as authApi from './auth'
import * as medicryptApi from './medicrypt'

export function useLogin() {
  const qc = useQueryClient()
  return useMutation(authApi.login, {
    onSuccess: () => {
      qc.invalidateQueries(['me'])
      qc.invalidateQueries(['records'])
    },
  })
}

export function useLogout() {
  return () => {
    authApi.logout()
  }
}

export function useListRecords() {
  return useQuery(['records'], medicryptApi.listRecords)
}

export function useUploadEncryptedRecord() {
  const qc = useQueryClient()
  return useMutation(medicryptApi.uploadEncryptedRecord, {
    onSuccess: () => qc.invalidateQueries(['records']),
  })
}

export function useGetPrediction(recordId: string | null) {
  return useQuery(['prediction', recordId], () => (recordId ? medicryptApi.getPrediction(recordId) : null), {
    enabled: !!recordId,
  })
}

export function useRegisteredKeys() {
  return useQuery(['registered-keys'], medicryptApi.getRegisteredKeys)
}
