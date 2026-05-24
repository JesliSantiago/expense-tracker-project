# expense-tracker-project

A personal finance and expense tracking app — Flutter mobile frontend backed by a FastAPI Python API.

## Structure

```
expense-tracker-project/
├── backend/          # FastAPI REST API
│   ├── app/
│   │   ├── main.py       # App entry point & middleware
│   │   ├── config.py     # Settings loaded from .env
│   │   ├── database.py   # SQLAlchemy engine & session
│   │   └── __init__.py
│   ├── requirements.txt
│   ├── .env              # Local secrets (git-ignored)
│   └── .env.example      # Template — safe to commit
└── mobile/           # Flutter app (run: flutter create mobile)
```

## Backend setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # then fill in SECRET_KEY
uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs` once running.

## Mobile setup

```bash
flutter create mobile
cd mobile
flutter run
```

## Database

Uses SQLite locally by default. To switch to PostgreSQL, update `DATABASE_URL` in `.env`:

```
DATABASE_URL=postgresql://user:password@localhost:5432/expense_tracker
```
