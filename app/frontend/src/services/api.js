const BASE_URL = import.meta.env.VITE_API_URL
const TOKEN_KEY = 'auth_token'

export function setAuthToken(token) {
  if (token) localStorage.setItem(TOKEN_KEY, token)
  else localStorage.removeItem(TOKEN_KEY)
}

function getAuthHeaders() {
  const token = localStorage.getItem(TOKEN_KEY)
  return token ? { Authorization: `Bearer ${token}` } : {}
}

async function request(path, options = {}) {
  if (!BASE_URL) {
    return { success: false, data: {}, error: 'VITE_API_URL no está configurada' }
  }

  try {
    const response = await fetch(`${BASE_URL}${path}`, {
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
        ...(options.headers || {}),
      },
      ...options,
    })

    const payload = await response
      .json()
      .catch(() => ({ success: false, data: {}, error: 'Respuesta inválida del servidor' }))

    if (!response.ok || !payload.success) {
      return {
        success: false,
        data: payload.data || {},
        error: payload.error || 'Error inesperado',
      }
    }

    return payload
  } catch (_error) {
    return { success: false, data: {}, error: 'No se pudo conectar con el backend' }
  }
}

export const api = {
  get: (path) => request(path),
  post: (path, data) => request(path, { method: 'POST', body: JSON.stringify(data) }),
  put: (path, data) => request(path, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (path) => request(path, { method: 'DELETE' }),
}
