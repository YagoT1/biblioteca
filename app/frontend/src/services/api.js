const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

async function request(path, options = {}) {
  try {
    const response = await fetch(`${BASE_URL}${path}`, {
      headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
      ...options,
    })

    const payload = await response.json().catch(() => ({ success: false, data: {}, error: 'Respuesta inválida del servidor' }))

    if (!response.ok || !payload.success) {
      return { success: false, data: payload.data || {}, error: payload.error || 'Error inesperado' }
    }

    return payload
  } catch (error) {
    return { success: false, data: {}, error: 'No se pudo conectar con el backend' }
  }
}

export const api = {
  get: (path) => request(path),
  post: (path, data) => request(path, { method: 'POST', body: JSON.stringify(data) }),
  put: (path, data) => request(path, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (path) => request(path, { method: 'DELETE' }),
}
