import Button from '../components/Button'
import Table from '../components/Table'

export default function PrestamosPage({ hook, notify }) {
  const { activos, vencidos, loading, error, devolverPrestamo } = hook

  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'libro_id', label: 'Libro ID' },
    { key: 'fecha_salida', label: 'Salida' },
    { key: 'fecha_vencimiento', label: 'Vencimiento' },
    {
      key: 'acciones',
      label: 'Acciones',
      render: (row) => (
        <Button
          variant="danger"
          disabled={!!row.fecha_devolucion}
          onClick={async () => {
            const result = await devolverPrestamo(row.id)
            notify(result.success ? 'success' : 'error', result.success ? 'Préstamo devuelto' : result.error)
          }}
        >
          Devolver
        </Button>
      ),
    },
  ]

  return (
    <section>
      <h1 className="mb-4 text-2xl font-bold text-slate-800">Préstamos</h1>
      {error ? <p className="mb-2 text-sm text-red-600">{error}</p> : null}
      {loading ? <p className="text-sm text-slate-500">Cargando préstamos...</p> : (
        <div className="space-y-6">
          <div>
            <h2 className="mb-2 text-lg font-semibold text-slate-700">Activos</h2>
            <Table columns={columns} rows={activos} emptyText="No hay préstamos activos" />
          </div>
          <div>
            <h2 className="mb-2 text-lg font-semibold text-slate-700">Vencidos</h2>
            <Table columns={columns} rows={vencidos} emptyText="No hay préstamos vencidos" />
          </div>
        </div>
      )}
    </section>
  )
}
