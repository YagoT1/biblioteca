# Biblioteca Fullstack

Repositorio monorepo con:

- `app/backend` (Flask + SQLAlchemy + PostgreSQL)
- `app/frontend` (React + Vite + Tailwind)

## Variables de entorno

### Backend (`app/backend/.env`)
- `DATABASE_URL`
- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `JWT_EXPIRES_HOURS`
- `TEST_DATABASE_URL` (opcional para testing)

### Frontend (`app/frontend/.env`)
- `VITE_API_URL`

## Ejecución local

### Backend
```bash
cd app/backend
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd app/frontend
npm install
npm run dev
```

## Deploy

### Render (backend)
- Root Directory: `app/backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`

### Vercel (frontend)
- Root Directory: `app/frontend`
- Build Command: `npm run build`
- Output Directory: `dist`
