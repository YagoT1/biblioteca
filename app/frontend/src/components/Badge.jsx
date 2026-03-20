export default function Badge({ estado, vencido = false }) {
  let color = 'bg-slate-200 text-slate-800'
  let text = estado

  if (vencido) {
    color = 'bg-amber-200 text-amber-800'
    text = 'VENCIDO'
  } else if (estado === 'DISPONIBLE') {
    color = 'bg-emerald-200 text-emerald-800'
  } else if (estado === 'PRESTADO') {
    color = 'bg-red-200 text-red-800'
  }

  return <span className={`rounded-full px-2 py-1 text-xs font-semibold ${color}`}>{text}</span>
}
