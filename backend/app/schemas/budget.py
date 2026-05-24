from pydantic import BaseModel, model_validator


class BudgetCreate(BaseModel):
    month: int   # 1–12
    year: int
    label: str | None = None

    @model_validator(mode="after")
    def validate_month(self):
        if not 1 <= self.month <= 12:
            raise ValueError("month must be between 1 and 12")
        return self


class BudgetOut(BaseModel):
    id: int
    user_id: int
    month: int
    year: int
    label: str | None

    model_config = {"from_attributes": True}


class BudgetUpdate(BaseModel):
    label: str | None = None
