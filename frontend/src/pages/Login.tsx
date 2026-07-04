import React from 'react'
import { useForm } from 'react-hook-form'
import { useNavigate } from 'react-router-dom'
import { useLogin } from '../api/hooks'

type FormValues = {
  email: string
  password: string
}

export default function Login() {
  const { register, handleSubmit } = useForm<FormValues>()
  const navigate = useNavigate()
  const login = useLogin()

  async function onSubmit(values: FormValues) {
    try {
      await login.mutateAsync(values)
      navigate('/')
    } catch (err) {
      // error handled by mutation state
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
      <div className="w-full max-w-md bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 className="text-2xl font-semibold mb-4">Sign in to Medicrypt</h2>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="block text-sm mb-1">Email</label>
            <input {...register('email')} type="email" className="w-full px-3 py-2 border rounded" />
          </div>

          <div>
            <label className="block text-sm mb-1">Password</label>
            <input {...register('password')} type="password" className="w-full px-3 py-2 border rounded" />
          </div>

          <div>
            <button
              type="submit"
              className="w-full px-4 py-2 bg-blue-600 text-white rounded"
              disabled={login.isLoading}
            >
              {login.isLoading ? 'Signing in…' : 'Sign in'}
            </button>
          </div>

          {login.isError && (
            <div className="text-sm text-red-600">{(login.error as any)?.response?.data?.detail || 'Login failed'}</div>
          )}
        </form>
      </div>
    </div>
  )
}
