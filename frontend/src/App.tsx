import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Landing from './pages/Landing'
import Login from './pages/Login'
import KeyManager from './pages/KeyManager'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/login" element={<Login />} />
      <Route path="/keys" element={<KeyManager />} />
    </Routes>
  )
}
