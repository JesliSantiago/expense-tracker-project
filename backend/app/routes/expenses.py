from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.budget import Budget
from app.models.expense import ExpenseCategory, ExpenseItem
from app.schemas.expense import (
    ExpenseCategoryCreate, ExpenseCategoryUpdate, ExpenseCategoryOut,
    ExpenseItemCreate, ExpenseItemUpdate, ExpenseItemOut,
)
from app.auth import get_current_user

router = APIRouter(tags=["expenses"])


def _get_owned_budget(budget_id: int, user: User, db: Session) -> Budget:
    budget = db.get(Budget, budget_id)
    if not budget or budget.user_id != user.id:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget


def _get_owned_category(category_id: int, budget_id: int, db: Session) -> ExpenseCategory:
    cat = db.get(ExpenseCategory, category_id)
    if not cat or cat.budget_id != budget_id:
        raise HTTPException(status_code=404, detail="Expense category not found")
    return cat


# ── Categories ────────────────────────────────────────────────────────────────

@router.get("/budgets/{budget_id}/expenses/categories", response_model=list[ExpenseCategoryOut])
def list_categories(budget_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _get_owned_budget(budget_id, user, db)
    return db.query(ExpenseCategory).filter(ExpenseCategory.budget_id == budget_id).order_by(ExpenseCategory.order).all()


@router.post("/budgets/{budget_id}/expenses/categories", response_model=ExpenseCategoryOut, status_code=status.HTTP_201_CREATED)
def add_category(budget_id: int, payload: ExpenseCategoryCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _get_owned_budget(budget_id, user, db)
    cat = ExpenseCategory(budget_id=budget_id, **payload.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@router.patch("/budgets/{budget_id}/expenses/categories/{category_id}", response_model=ExpenseCategoryOut)
def update_category(budget_id: int, category_id: int, payload: ExpenseCategoryUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _get_owned_budget(budget_id, user, db)
    cat = _get_owned_category(category_id, budget_id, db)
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(cat, field, value)
    db.commit()
    db.refresh(cat)
    return cat


@router.delete("/budgets/{budget_id}/expenses/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(budget_id: int, category_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _get_owned_budget(budget_id, user, db)
    cat = _get_owned_category(category_id, budget_id, db)
    db.delete(cat)
    db.commit()


# ── Items ─────────────────────────────────────────────────────────────────────

@router.post("/budgets/{budget_id}/expenses/categories/{category_id}/items", response_model=ExpenseItemOut, status_code=status.HTTP_201_CREATED)
def add_item(budget_id: int, category_id: int, payload: ExpenseItemCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _get_owned_budget(budget_id, user, db)
    _get_owned_category(category_id, budget_id, db)
    item = ExpenseItem(category_id=category_id, **payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.patch("/budgets/{budget_id}/expenses/items/{item_id}", response_model=ExpenseItemOut)
def update_item(budget_id: int, item_id: int, payload: ExpenseItemUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _get_owned_budget(budget_id, user, db)
    item = db.get(ExpenseItem, item_id)
    if not item or item.category.budget_id != budget_id:
        raise HTTPException(status_code=404, detail="Expense item not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/budgets/{budget_id}/expenses/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(budget_id: int, item_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _get_owned_budget(budget_id, user, db)
    item = db.get(ExpenseItem, item_id)
    if not item or item.category.budget_id != budget_id:
        raise HTTPException(status_code=404, detail="Expense item not found")
    db.delete(item)
    db.commit()
