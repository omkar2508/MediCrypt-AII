import React, { useEffect, useState } from 'react'
import { createKey, listKeys, deleteKey, exportEvaluationKey, exportSecretForBackup } from '../crypto/keyManager'
import { useRegisteredKeys } from '../api/hooks'

export default function KeyManager() {
  const [keys, setKeys] = useState<Array<{ key_id: string; created_at: string }>>([])
  const [selected, setSelected] = useState<string | null>(null)
  const [evalKey, setEvalKey] = useState<string | null>(null)
  const regKeys = useRegisteredKeys()

  useEffect(() => {
    setKeys(listKeys())
  }, [])

  async function handleCreate() {
    const k = createKey()
    setKeys(listKeys())
    setSelected(k.key_id)
    const ev = await exportEvaluationKey(k.key_id)
    setEvalKey(ev)
  }

  async function handleShow(key_id: string) {
    setSelected(key_id)
    const ev = await exportEvaluationKey(key_id)
    setEvalKey(ev)
  }

  function handleDelete(key_id: string) {
    if (!confirm('Delete key ' + key_id + '? This cannot be undone.')) return
    deleteKey(key_id)
    setKeys(listKeys())
    if (selected === key_id) {
      setSelected(null)
      setEvalKey(null)
    }
  }

  function handleCopy(text: string) {
    navigator.clipboard.writeText(text)
  }

  function handleExportSecret(key_id: string) {
    const b64 = exportSecretForBackup(key_id)
    // show secret in new window for manual copy (explicit action)
    const w = window.open('', '_blank')
    if (w) w.document.body.innerText = b64
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-semibold">Client Key Manager</h2>
        <div>
          <button onClick={handleCreate} className="px-4 py-2 bg-green-600 text-white rounded">Create Key</button>
        </div>
      </div>

      <p className="mb-4 text-sm opacity-80">Keys generated here are secret and never leave your browser. You should register the generated evaluation key with the server (copy & paste) so the server can evaluate on your ciphertext without access to your secret key.</p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h3 className="font-semibold mb-2">Saved Keys</h3>
          <div className="space-y-2">
            {keys.length === 0 && <div className="p-4 bg-gray-50 rounded">No keys yet.</div>}
            {keys.map((k) => (
              <div key={k.key_id} className="p-3 border rounded flex items-center justify-between">
                <div>
                  <div className="font-mono text-sm">{k.key_id}</div>
                  <div className="text-xs opacity-70">{new Date(k.created_at).toLocaleString()}</div>
                </div>
                <div className="flex gap-2">
                  <button onClick={() => handleShow(k.key_id)} className="px-3 py-1 border rounded">Show</button>
                  <button onClick={() => handleExportSecret(k.key_id)} className="px-3 py-1 border rounded">Export Secret</button>
                  <button onClick={() => handleDelete(k.key_id)} className="px-3 py-1 text-red-600">Delete</button>
                </div>
              </div>
            ))}
          </div>
        </div>

          <div>
          <h3 className="font-semibold mb-2">Selected Key</h3>
          {selected ? (
            <div className="p-4 bg-white dark:bg-gray-800 rounded border">
              <div className="mb-2 text-sm">Key ID</div>
              <div className="font-mono mb-4">{selected}</div>

              <div className="mb-2 text-sm">Public Evaluation Key (SHA256)</div>
              <div className="font-mono break-all mb-4">{evalKey}</div>

              <div className="flex gap-2">
                <button onClick={() => evalKey && handleCopy(evalKey)} className="px-3 py-1 border rounded">Copy Eval Key</button>
                <button
                  onClick={async () => {
                    if (!selected || !evalKey) return
                    try {
                      // send the evalKey (base64) to server as bytes
                      const mod = await import('../api/medicrypt')
                      await mod.registerEvaluationKey(selected, evalKey)
                      alert('Evaluation key registered successfully')
                    } catch (err: any) {
                      alert('Registration failed: ' + (err?.response?.data?.detail || err?.message || err))
                    }
                  }}
                  className="px-3 py-1 border rounded"
                >
                  Register
                </button>
              </div>
            </div>
          ) : (
            <div className="p-4 bg-gray-50 rounded">No key selected.</div>
          )}

            <div className="mt-6 text-xs opacity-70">Warning: The server should never ask for your secret key. Keep backups of your secret outside the browser if needed.</div>
        </div>
      </div>

        <section className="mt-8">
          <h3 className="font-semibold mb-2">Server Registered Keys</h3>
          <div className="p-4 bg-white dark:bg-gray-800 rounded border">
            {regKeys.isLoading && <div>Loading...</div>}
            {regKeys.isError && <div className="text-red-600">Failed to load registered keys</div>}
            {regKeys.data && regKeys.data.length === 0 && <div>No registered keys on server.</div>}
            {regKeys.data && regKeys.data.length > 0 && (
              <div className="space-y-2">
                {regKeys.data.map((k: any) => (
                  <div key={k.key_id} className="p-2 border rounded flex items-center justify-between">
                    <div>
                      <div className="font-mono text-sm">{k.key_id}</div>
                      <div className="text-xs opacity-70">{new Date(k.created_at).toLocaleString()}</div>
                    </div>
                    <div className="text-sm">{k.revoked ? 'revoked' : k.version}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </section>
    </div>
  )
}
