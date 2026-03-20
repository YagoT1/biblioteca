export default function Input({ label, error, ...props }) {
  return (
    <label className="flex w-full flex-col gap-1 text-sm">
      <span className="font-medium text-slate-700">{label}</span>
      <input
        className="rounded-md border border-slate-300 px-3 py-2 outline-none ring-blue-500 focus:ring"
        {...props}
      />
      {error ? <span className="text-xs text-red-600">{error}</span> : null}
    </label>
  )
}
