from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.budget import Budget
from app.schemas.budget import BudgetCreate, BudgetOut, BudgetUpdate
from app.auth import get_current_user

router = APIRouter(prefix="/budgets", tags=["budgets"])


def _get_owned_budget(budget_id: int, user: User, db: Session) -> Budget:
    budget = db.get(Budget, budget_id)
    if not budget or budget.user_id != user.id:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget


@router.get("", response_model=list[BudgetOut])
def list_budgets(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Budget).filter(Budget.user_id == user.id).order_by(Budget.year.desc(), Budget.month.desc()).all()


@router.post("", response_model=BudgetOut, status_code=status.HTTP_201_CREATED)
def create_budget(payload: BudgetCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    existing = db.query(Budget).filter(
        Budget.user_id == user.id,
        Budget.month == payload.month,
        Budget.year == payload.year,
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Budget for that month/year already exists")
    budget = Budget(user_id=user.id, **payload.model_dump())
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


@router.get("/{budget_id}", response_model=BudgetOut)
def get_budget(budget_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return _get_owned_budget(budget_id, user, db)


@router.patch("/{budget_id}", response_model=BudgetOut)
def update_budget(budget_id: int, payload: BudgetUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    budget = _get_owned_budget(budget_id, user, db)
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(budget, field, value)
    db.commit()
    db.refresh(budget)
    return budget


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(budget_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    budget = _get_owned_budget(budget_id, user, db)
    db.delete(budget)
    db.commit()
