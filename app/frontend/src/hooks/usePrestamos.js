import { useCallback, useEffect, useState } from 'react'
import { api } from '../services/api'

export function usePrestamos() {
  const [activos, setActivos] = useState([])
  const [vencidos, setVencidos] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const fetchPrestamos = useCallback(async () => {
    setLoading(true)
    setError(null)

    const [activosResp, vencidosResp] = await Promise.all([
      api.get('/prestamos/activos'),
      api.get('/prestamos/vencidos'),
    ])

    if (!activosResp.success || !vencidosResp.success) {
      setError(activosResp.error || vencidosResp.error)
    } else {
      setActivos(activosResp.data)
      setVencidos(vencidosResp.data)
    }

    setLoading(false)
  }, [])

  const devolverPrestamo = useCallback(async (id) => {
    const result = await api.post(`/prestamos/${id}/devolver`, {})
    if (!result.success) return result
    await fetchPrestamos()
    return result
  }, [fetchPrestamos])

  useEffect(() => {
    fetchPrestamos()
  }, [fetchPrestamos])

  return { activos, vencidos, loading, error, fetchPrestamos, devolverPrestamo }
}
