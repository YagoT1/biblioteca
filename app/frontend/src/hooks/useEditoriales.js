import { useCallback, useEffect, useState } from 'react'
import { api } from '../services/api'

export function useEditoriales() {
  const [editoriales, setEditoriales] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const fetchEditoriales = useCallback(async () => {
    setLoading(true)
    setError(null)
    const result = await api.get('/editoriales')
    if (!result.success) {
      setError(result.error)
    } else {
      setEditoriales(result.data)
    }
    setLoading(false)
  }, [])

  const createEditorial = useCallback(async (payload) => {
    const result = await api.post('/editoriales', payload)
    if (!result.success) return result
    await fetchEditoriales()
    return result
  }, [fetchEditoriales])

  const updateEditorial = useCallback(async (id, payload) => {
    const result = await api.put(`/editoriales/${id}`, payload)
    if (!result.success) return result
    await fetchEditoriales()
    return result
  }, [fetchEditoriales])

  const deleteEditorial = useCallback(async (id) => {
    const result = await api.delete(`/editoriales/${id}`)
    if (!result.success) return result
    await fetchEditoriales()
    return result
  }, [fetchEditoriales])

  useEffect(() => {
    fetchEditoriales()
  }, [fetchEditoriales])

  return { editoriales, loading, error, fetchEditoriales, createEditorial, updateEditorial, deleteEditorial }
}
