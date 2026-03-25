import Sidebar from '../components/Sidebar'

export default function AdminLayout({ activePage, onPageChange, children }) {
  return (
    <div className="min-h-screen bg-slate-100 md:flex">
      <Sidebar active={activePage} onChange={onPageChange} />
      <main className="flex-1 p-4 md:p-6">{children}</main>
    </div>
  )
}
