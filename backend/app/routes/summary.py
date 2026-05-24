from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.budget import Budget
from app.models.income import IncomeEntry
from app.models.saving import SavingEntry
from app.models.expense import ExpenseItem
from app.schemas.summary import BudgetSummary
from app.auth import get_current_user

router = APIRouter(tags=["summary"])


@router.get("/budgets/{budget_id}/summary", response_model=BudgetSummary)
def get_summary(budget_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    budget = db.get(Budget, budget_id)
    if not budget or budget.user_id != user.id:
        raise HTTPException(status_code=404, detail="Budget not found")

    income_entries = db.query(IncomeEntry).filter(IncomeEntry.budget_id == budget_id).all()
    saving_entries = db.query(SavingEntry).filter(SavingEntry.budget_id == budget_id).all()

    # collect all expense items across all categories
    expense_items = (
        db.query(ExpenseItem)
        .join(ExpenseItem.category)
        .filter_by(budget_id=budget_id)
        .all()
    )

    total_income_proj = sum(e.projected for e in income_entries)
    total_income_act  = sum(e.actual    for e in income_entries)

    total_savings_proj = sum(e.projected for e in saving_entries)
    total_savings_act  = sum(e.actual    for e in saving_entries)

    total_exp_proj = sum(e.projected for e in expense_items)
    total_exp_act  = sum(e.actual    for e in expense_items)

    net_proj = total_income_proj - total_exp_proj
    net_act  = total_income_act  - total_exp_act

    pct_proj = (total_savings_proj / total_income_proj * 100) if total_income_proj else 0.0
    pct_act  = (total_savings_act  / total_income_act  * 100) if total_income_act  else 0.0

    disposable_proj = total_income_proj - total_savings_proj - total_exp_proj
    disposable_act  = total_income_act  - total_savings_act  - total_exp_act

    return BudgetSummary(
        total_income_projected=total_income_proj,
        total_income_actual=total_income_act,
        total_savings_projected=total_savings_proj,
        total_savings_actual=total_savings_act,
        total_expenses_projected=total_exp_proj,
        total_expenses_actual=total_exp_act,
        net_projected=net_proj,
        net_actual=net_act,
        pct_income_saved_projected=round(pct_proj, 2),
        pct_income_saved_actual=round(pct_act, 2),
        disposable_projected=disposable_proj,
        disposable_actual=disposable_act,
    )
