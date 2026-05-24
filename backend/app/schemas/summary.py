from pydantic import BaseModel


class BudgetSummary(BaseModel):
    total_income_projected: float
    total_income_actual: float

    total_savings_projected: float
    total_savings_actual: float

    total_expenses_projected: float
    total_expenses_actual: float

    # income - expenses (what's left to spend / save)
    net_projected: float
    net_actual: float

    # (savings / income) * 100
    pct_income_saved_projected: float
    pct_income_saved_actual: float

    # income - savings - expenses
    disposable_projected: float
    disposable_actual: float
