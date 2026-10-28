# E-Pharmacy Management System

## Project Structure

```
e-pharmacy/
├── backend/        # FastAPI — API server, business logic, DB access
├── frontend/
│   ├── pos/        # React — Point of Sale interface
│   └── erp/        # React — Backend ERP dashboard
└── uploads/        # Prescription scan storage (runtime, not committed)
```

## Stack

| Layer      | Technology              |
|------------|-------------------------|
| API        | Python 3.11 + FastAPI   |
| Database   | PostgreSQL 16           |
| Migrations | Alembic                 |
| POS UI     | React 18 + Vite + TS    |
| ERP UI     | React 18 + Vite + TS    |
| Auth       | JWT (role-based)        |

## Getting Started

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # fill in your values
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

### POS Frontend

```bash
cd frontend/pos
npm install
npm run dev   # runs on http://localhost:5173
```

### ERP Frontend

```bash
cd frontend/erp
npm install
npm run dev   # runs on http://localhost:5174
```
