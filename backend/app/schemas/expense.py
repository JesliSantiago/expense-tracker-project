from pydantic import BaseModel, computed_field


class ExpenseItemCreate(BaseModel):
    name: str
    projected: float = 0.0
    actual: float = 0.0
    order: int = 0


class ExpenseItemUpdate(BaseModel):
    name: str | None = None
    projected: float | None = None
    actual: float | None = None
    order: int | None = None


class ExpenseItemOut(BaseModel):
    id: int
    category_id: int
    name: str
    projected: float
    actual: float
    order: int

    @computed_field
    @property
    def difference(self) -> float:
        return self.actual - self.projected

    model_config = {"from_attributes": True}


class ExpenseCategoryCreate(BaseModel):
    name: str
    order: int = 0


class ExpenseCategoryUpdate(BaseModel):
    name: str | None = None
    order: int | None = None


class ExpenseCategoryOut(BaseModel):
    id: int
    budget_id: int
    name: str
    order: int
    items: list[ExpenseItemOut] = []

    model_config = {"from_attributes": True}
