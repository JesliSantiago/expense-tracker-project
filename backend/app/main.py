from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import Base, engine
from app.routes import auth, budgets, income, savings, expenses, summary

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(budgets.router)
app.include_router(income.router)
app.include_router(savings.router)
app.include_router(expenses.router)
app.include_router(summary.router)


@app.get("/health")
def health():
    return {"status": "ok"}
