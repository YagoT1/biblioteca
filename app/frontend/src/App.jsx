import { useMemo, useState } from 'react'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import ProtectedRoute from './components/ProtectedRoute'
import { useEditoriales } from './hooks/useEditoriales'
import { useLibros } from './hooks/useLibros'
import { usePrestamos } from './hooks/usePrestamos'
import AdminLayout from './layouts/AdminLayout'
import DashboardPage from './pages/DashboardPage'
import EditorialesPage from './pages/EditorialesPage'
import LibrosPage from './pages/LibrosPage'
import LoginPage from './pages/LoginPage'
import PrestamosPage from './pages/PrestamosPage'

function Alert({ alert, onClose }) {
  if (!alert) return null
  const base = alert.type === 'error' ? 'bg-red-100 text-red-800' : 'bg-emerald-100 text-emerald-800'
  return (
    <div className={`mb-4 flex items-center justify-between rounded-md px-3 py-2 text-sm ${base}`}>
      <span>{alert.message}</span>
      <button className="font-semibold" onClick={onClose}>x</button>
    </div>
  )
}

function AdminApp() {
  const [page, setPage] = useState('dashboard')
  const [alert, setAlert] = useState(null)

  const librosHook = useLibros()
  const editorialesHook = useEditoriales()
  const prestamosHook = usePrestamos()

  const notify = (type, message) => {
    setAlert({ type, message })
    setTimeout(() => setAlert(null), 3000)
    if (type === 'success') {
      prestamosHook.fetchPrestamos()
      librosHook.fetchLibros()
    }
  }

  const pageComponent = useMemo(() => {
    if (page === 'libros') return <LibrosPage librosHook={librosHook} editorialesHook={editorialesHook} notify={notify} />
    if (page === 'editoriales') return <EditorialesPage hook={editorialesHook} notify={notify} />
    if (page === 'prestamos') return <PrestamosPage hook={prestamosHook} notify={notify} />
    return <DashboardPage metrics={librosHook.metrics} />
  }, [page, librosHook, editorialesHook, prestamosHook])

  return (
    <AdminLayout activePage={page} onPageChange={setPage}>
      <Alert alert={alert} onClose={() => setAlert(null)} />
      {pageComponent}
    </AdminLayout>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/"
          element={(
            <ProtectedRoute>
              <AdminApp />
            </ProtectedRoute>
          )}
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
