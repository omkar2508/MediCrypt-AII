import React from 'react'

export default function Landing() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      <header className="max-w-6xl mx-auto p-6 flex justify-between items-center">
        <h1 className="text-2xl font-semibold">Medicrypt AI</h1>
        <nav>
          <a href="/login" className="text-sm opacity-80 hover:opacity-100">Login</a>
        </nav>
      </header>

      <main className="max-w-6xl mx-auto p-6">
        <section className="py-20 flex flex-col md:flex-row items-center gap-8">
          <div className="flex-1">
            <h2 className="text-4xl font-bold mb-4">Privacy-first medical AI, powered by FHE</h2>
            <p className="text-lg opacity-80 mb-6">Keep patient data encrypted at all times. Perform predictions on ciphertext without revealing private data.</p>
            <div className="flex gap-4">
              <a className="px-6 py-3 bg-blue-600 text-white rounded shadow" href="#">Get Started</a>
              <a className="px-6 py-3 border rounded" href="#">Learn More</a>
            </div>
          </div>
          <div className="flex-1 bg-white dark:bg-gray-800 rounded-lg p-8 shadow">
            <h3 className="text-xl font-semibold mb-2">Live demo</h3>
            <p className="mb-4 opacity-80">Upload encrypted medical data and receive an encrypted prediction you can decrypt locally.</p>
            <div className="h-40 bg-gray-100 dark:bg-gray-700 rounded flex items-center justify-center">Demo preview</div>
          </div>
        </section>

        <section className="py-8">
          <h3 className="text-2xl font-semibold mb-4">How it works</h3>
          <ol className="list-decimal ml-6 space-y-2">
            <li>Generate keys locally on the client</li>
            <li>Encrypt medical features</li>
            <li>Upload ciphertext to server</li>
            <li>Server computes on ciphertext and returns encrypted result</li>
            <li>Client decrypts and shows the prediction</li>
          </ol>
        </section>
      </main>

      <footer className="border-t mt-12 py-6 text-center">
        <small className="opacity-70">© Medicrypt AI</small>
      </footer>
    </div>
  )
}
