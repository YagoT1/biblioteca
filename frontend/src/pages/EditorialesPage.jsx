import { useState } from 'react'
import Button from '../components/Button'
import Input from '../components/Input'
import Modal from '../components/Modal'
import Table from '../components/Table'

function emptyEditorial() {
  return { nombre: '', pais: '', estado: 'activo' }
}

export default function EditorialesPage({ hook, notify }) {
  const { editoriales, loading, error, createEditorial, updateEditorial, deleteEditorial } = hook
  const [open, setOpen] = useState(false)
  const [editId, setEditId] = useState(null)
  const [form, setForm] = useState(emptyEditorial())

  const submit = async (e) => {
    e.preventDefault()
    const result = editId ? await updateEditorial(editId, form) : await createEditorial(form)
    notify(result.success ? 'success' : 'error', result.success ? 'Editorial guardada' : result.error)
    if (result.success) {
      setOpen(false)
      setEditId(null)
      setForm(emptyEditorial())
    }
  }

  const columns = [
    { key: 'nombre', label: 'Nombre' },
    { key: 'pais', label: 'País' },
    { key: 'estado', label: 'Estado' },
    {
      key: 'acciones',
      label: 'Acciones',
      render: (row) => (
        <div className="flex gap-2">
          <Button variant="secondary" onClick={() => { setEditId(row.id); setForm({ nombre: row.nombre || '', pais: row.pais || '', estado: row.estado || 'activo' }); setOpen(true) }}>
            Editar
          </Button>
          <Button variant="danger" onClick={async () => {
            const result = await deleteEditorial(row.id)
            notify(result.success ? 'success' : 'error', result.success ? 'Editorial inactivada' : result.error)
          }}>
            Inactivar
          </Button>
        </div>
      ),
    },
  ]

  return (
    <section>
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-800">Editoriales</h1>
        <Button onClick={() => { setEditId(null); setForm(emptyEditorial()); setOpen(true) }}>Nueva editorial</Button>
      </div>
      {error ? <p className="mb-2 text-sm text-red-600">{error}</p> : null}
      {loading ? <p className="text-sm text-slate-500">Cargando editoriales...</p> : <Table columns={columns} rows={editoriales} />}

      <Modal open={open} title={editId ? 'Editar editorial' : 'Nueva editorial'} onClose={() => setOpen(false)}>
        <form className="grid gap-3" onSubmit={submit}>
          <Input label="Nombre" value={form.nombre} onChange={(e) => setForm({ ...form, nombre: e.target.value })} required />
          <Input label="País" value={form.pais} onChange={(e) => setForm({ ...form, pais: e.target.value })} />
          <label className="text-sm">
            <span className="mb-1 block font-medium text-slate-700">Estado</span>
            <select className="w-full rounded-md border border-slate-300 px-3 py-2" value={form.estado} onChange={(e) => setForm({ ...form, estado: e.target.value })}>
              <option value="activo">Activo</option>
              <option value="inactivo">Inactivo</option>
            </select>
          </label>
          <Button type="submit">Guardar</Button>
        </form>
      </Modal>
    </section>
  )
}
