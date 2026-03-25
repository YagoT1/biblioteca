import { useCallback, useEffect, useMemo, useState } from 'react'
import { api } from '../services/api'

export function useLibros() {
  const [libros, setLibros] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const fetchLibros = useCallback(async () => {
    setLoading(true)
    setError(null)
    const result = await api.get('/libros')
    if (!result.success) {
      setError(result.error)
    } else {
      setLibros(result.data)
    }
    setLoading(false)
  }, [])

  const createLibro = useCallback(async (payload) => {
    const result = await api.post('/libros', payload)
    if (!result.success) return result
    await fetchLibros()
    return result
  }, [fetchLibros])

  const updateLibro = useCallback(async (id, payload) => {
    const result = await api.put(`/libros/${id}`, payload)
    if (!result.success) return result
    await fetchLibros()
    return result
  }, [fetchLibros])

  const prestarLibro = useCallback(async (libroId, fecha_vencimiento) => {
    const result = await api.post('/prestamos', { libro_id: libroId, fecha_vencimiento })
    if (!result.success) return result
    await fetchLibros()
    return result
  }, [fetchLibros])

  const devolverPrestamo = useCallback(async (prestamoId) => {
    const result = await api.post(`/prestamos/${prestamoId}/devolver`, {})
    if (!result.success) return result
    await fetchLibros()
    return result
  }, [fetchLibros])

  useEffect(() => {
    fetchLibros()
  }, [fetchLibros])

  const metrics = useMemo(() => {
    const disponibles = libros.filter((l) => l.estado === 'DISPONIBLE').length
    const prestados = libros.filter((l) => l.estado === 'PRESTADO').length
    const vencidos = libros.filter((l) => l.vencido).length
    return { disponibles, prestados, vencidos }
  }, [libros])

  return { libros, loading, error, fetchLibros, createLibro, updateLibro, prestarLibro, devolverPrestamo, metrics }
}
