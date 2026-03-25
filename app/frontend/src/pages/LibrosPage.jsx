import { useMemo, useState } from 'react'
import Badge from '../components/Badge'
import Button from '../components/Button'
import Input from '../components/Input'
import Modal from '../components/Modal'
import Table from '../components/Table'

function emptyForm() {
  return { titulo: '', autor: '', editorial_id: '', isbn: '', categoria: '', ubicacion: '' }
}

export default function LibrosPage({ librosHook, editorialesHook, notify }) {
  const { libros, loading, error, createLibro, prestarLibro, devolverPrestamo } = librosHook
  const { editoriales } = editorialesHook
  const [search, setSearch] = useState('')
  const [openLibroModal, setOpenLibroModal] = useState(false)
  const [openPrestamoModal, setOpenPrestamoModal] = useState(false)
  const [form, setForm] = useState(emptyForm())
  const [prestamo, setPrestamo] = useState({ libroId: null, fecha_vencimiento: '' })

  const filtered = useMemo(() => {
    const q = search.toLowerCase().trim()
    if (!q) return libros
    return libros.filter((l) =>
      [l.titulo, l.autor, l.isbn].some((v) => (v || '').toLowerCase().includes(q)),
    )
  }, [libros, search])

  const columns = [
    { key: 'titulo', label: 'Título' },
    { key: 'autor', label: 'Autor' },
    { key: 'isbn', label: 'ISBN' },
    {
      key: 'estado',
      label: 'Estado',
      render: (row) => <Badge estado={row.estado} vencido={row.vencido} />,
    },
    {
      key: 'acciones',
      label: 'Acciones',
      render: (row) => (
        <div className="flex gap-2">
          {row.estado === 'DISPONIBLE' ? (
            <Button
              variant="success"
              onClick={() => {
                setPrestamo({ libroId: row.id, fecha_vencimiento: '' })
                setOpenPrestamoModal(true)
              }}
            >
              Prestar
            </Button>
          ) : (
            <Button
              variant="danger"
              disabled={!row.prestamo_id}
              onClick={async () => {
                const r = await devolverPrestamo(row.prestamo_id)
                notify(r.success ? 'success' : 'error', r.success ? 'Libro devuelto' : r.error)
              }}
            >
              Devolver
            </Button>
          )}
        </div>
      ),
    },
  ]

  const submitLibro = async (e) => {
    e.preventDefault()
    const payload = {
      ...form,
      editorial_id: form.editorial_id ? Number(form.editorial_id) : null,
    }
    const result = await createLibro(payload)
    notify(result.success ? 'success' : 'error', result.success ? 'Libro creado' : result.error)
    if (result.success) {
      setForm(emptyForm())
      setOpenLibroModal(false)
    }
  }

  const submitPrestamo = async (e) => {
    e.preventDefault()
    const result = await prestarLibro(prestamo.libroId, prestamo.fecha_vencimiento)
    notify(result.success ? 'success' : 'error', result.success ? 'Préstamo registrado' : result.error)
    if (result.success) setOpenPrestamoModal(false)
  }

  return (
    <section>
      <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
        <h1 className="text-2xl font-bold text-slate-800">Libros</h1>
        <div className="flex gap-2">
          <Input label="Buscar" value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Título, autor o ISBN" />
          <Button onClick={() => setOpenLibroModal(true)}>Nuevo libro</Button>
        </div>
      </div>

      {error ? <p className="mb-2 text-sm text-red-600">{error}</p> : null}
      {loading ? <p className="text-sm text-slate-500">Cargando libros...</p> : <Table columns={columns} rows={filtered} />}

      <Modal open={openLibroModal} title="Crear libro" onClose={() => setOpenLibroModal(false)}>
        <form className="grid gap-3" onSubmit={submitLibro}>
          <Input label="Título" value={form.titulo} onChange={(e) => setForm({ ...form, titulo: e.target.value })} required />
          <Input label="Autor" value={form.autor} onChange={(e) => setForm({ ...form, autor: e.target.value })} required />
          <Input label="ISBN" value={form.isbn} onChange={(e) => setForm({ ...form, isbn: e.target.value })} />
          <Input label="Categoría" value={form.categoria} onChange={(e) => setForm({ ...form, categoria: e.target.value })} />
          <Input label="Ubicación" value={form.ubicacion} onChange={(e) => setForm({ ...form, ubicacion: e.target.value })} />
          <label className="text-sm">
            <span className="mb-1 block font-medium text-slate-700">Editorial</span>
            <select
              className="w-full rounded-md border border-slate-300 px-3 py-2"
              value={form.editorial_id}
              onChange={(e) => setForm({ ...form, editorial_id: e.target.value })}
            >
              <option value="">Sin editorial</option>
              {editoriales.map((ed) => (
                <option key={ed.id} value={ed.id}>{ed.nombre}</option>
              ))}
            </select>
          </label>
          <Button type="submit">Guardar</Button>
        </form>
      </Modal>

      <Modal open={openPrestamoModal} title="Registrar préstamo" onClose={() => setOpenPrestamoModal(false)}>
        <form className="grid gap-3" onSubmit={submitPrestamo}>
          <Input
            label="Fecha vencimiento (ISO-8601)"
            placeholder="2026-12-31T18:00:00+00:00"
            value={prestamo.fecha_vencimiento}
            onChange={(e) => setPrestamo({ ...prestamo, fecha_vencimiento: e.target.value })}
            required
          />
          <Button type="submit" variant="success">Confirmar préstamo</Button>
        </form>
      </Modal>
    </section>
  )
}
