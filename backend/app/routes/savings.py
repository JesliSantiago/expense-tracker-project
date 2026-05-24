from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.budget import Budget
from app.models.saving import SavingEntry
from app.schemas.saving import SavingEntryCreate, SavingEntryUpdate, SavingEntryOut
from app.auth import get_current_user

router = APIRouter(prefix="/budgets/{budget_id}/savings", tags=["savings"])


def _get_owned_budget(budget_id: int, user: User, db: Session) -> Budget:
    budget = db.get(Budget, budget_id)
    if not budget or budget.user_id != user.id:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget


@router.get("", response_model=list[SavingEntryOut])
def list_savings(budget_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _get_owned_budget(budget_id, user, db)
    return db.query(SavingEntry).filter(SavingEntry.budget_id == budget_id).order_by(SavingEntry.order).all()


@router.post("", response_model=SavingEntryOut, status_code=status.HTTP_201_CREATED)
def add_saving(budget_id: int, payload: SavingEntryCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _get_owned_budget(budget_id, user, db)
    entry = SavingEntry(budget_id=budget_id, **payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.patch("/{entry_id}", response_model=SavingEntryOut)
def update_saving(budget_id: int, entry_id: int, payload: SavingEntryUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _get_owned_budget(budget_id, user, db)
    entry = db.get(SavingEntry, entry_id)
    if not entry or entry.budget_id != budget_id:
        raise HTTPException(status_code=404, detail="Saving entry not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(entry, field, value)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_saving(budget_id: int, entry_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _get_owned_budget(budget_id, user, db)
    entry = db.get(SavingEntry, entry_id)
    if not entry or entry.budget_id != budget_id:
        raise HTTPException(status_code=404, detail="Saving entry not found")
    db.delete(entry)
    db.commit()
