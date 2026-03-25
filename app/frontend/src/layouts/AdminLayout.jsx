import Button from '../components/Button'
import Sidebar from '../components/Sidebar'
import { clearAuthToken } from '../utils/auth'

export default function AdminLayout({ activePage, onPageChange, children }) {
  const onLogout = () => {
    clearAuthToken()
    window.location.assign('/login')
  }

  return (
    <div className="min-h-screen bg-slate-100 md:flex">
      <Sidebar active={activePage} onChange={onPageChange} />
      <main className="flex-1 p-4 md:p-6">
        <div className="mb-4 flex justify-end">
          <Button variant="secondary" onClick={onLogout}>Salir</Button>
        </div>
        {children}
      </main>
    </div>
  )
}
