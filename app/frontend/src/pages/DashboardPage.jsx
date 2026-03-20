export default function DashboardPage({ metrics }) {
  const cards = [
    { label: 'Libros disponibles', value: metrics.disponibles, color: 'bg-emerald-500' },
    { label: 'Libros prestados', value: metrics.prestados, color: 'bg-red-500' },
    { label: 'Vencidos', value: metrics.vencidos, color: 'bg-amber-500' },
  ]

  return (
    <section>
      <h1 className="mb-4 text-2xl font-bold text-slate-800">Dashboard</h1>
      <div className="grid gap-4 md:grid-cols-3">
        {cards.map((card) => (
          <div key={card.label} className="rounded-lg bg-white p-4 shadow">
            <div className={`mb-3 h-1 w-16 rounded ${card.color}`} />
            <p className="text-sm text-slate-500">{card.label}</p>
            <p className="text-3xl font-bold text-slate-800">{card.value}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
