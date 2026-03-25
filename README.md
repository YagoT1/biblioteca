# Biblioteca Fullstack

Repositorio monorepo con:

- `app/backend` (Flask + SQLAlchemy + PostgreSQL)
- `app/frontend` (React + Vite + Tailwind)

## Variables de entorno

### Backend (`app/backend/.env`)
- `DATABASE_URL`
- `TEST_DATABASE_URL`
- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `JWT_EXPIRES_HOURS`

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
