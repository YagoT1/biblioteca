import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Button from '../components/Button'
import Input from '../components/Input'
import { api, setAuthToken } from '../services/api'

export default function LoginPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  const onSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    const result = await api.post('/login', { username, password })
    if (!result.success) {
      setError(result.error)
      setLoading(false)
      return
    }

    setAuthToken(result.data.token)
    navigate('/', { replace: true })
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-100 p-4">
      <form onSubmit={onSubmit} className="w-full max-w-md space-y-3 rounded-lg bg-white p-6 shadow">
        <h1 className="text-xl font-bold text-slate-800">Login administrador</h1>
        <Input label="Usuario" value={username} onChange={(e) => setUsername(e.target.value)} required />
        <Input label="Contraseña" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        {error ? <p className="text-sm text-red-600">{error}</p> : null}
        <Button type="submit" className="w-full" disabled={loading}>
          {loading ? 'Ingresando...' : 'Ingresar'}
        </Button>
      </form>
    </div>
  )
}
