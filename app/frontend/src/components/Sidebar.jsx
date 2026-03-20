import { NAV_ITEMS } from '../utils/constants'

export default function Sidebar({ active, onChange }) {
  return (
    <aside className="w-full border-r bg-white md:w-64">
      <div className="border-b px-4 py-4 text-lg font-bold text-slate-800">Biblioteca Popular</div>
      <nav className="p-3">
        {NAV_ITEMS.map((item) => (
          <button
            key={item.key}
            onClick={() => onChange(item.key)}
            className={`mb-1 w-full rounded-md px-3 py-2 text-left text-sm font-medium ${
              active === item.key ? 'bg-blue-100 text-blue-700' : 'text-slate-700 hover:bg-slate-100'
            }`}
          >
            {item.label}
          </button>
        ))}
      </nav>
    </aside>
  )
}
