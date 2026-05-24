from pydantic import BaseModel, computed_field


class SavingEntryCreate(BaseModel):
    name: str
    projected: float = 0.0
    actual: float = 0.0
    order: int = 0


class SavingEntryUpdate(BaseModel):
    name: str | None = None
    projected: float | None = None
    actual: float | None = None
    order: int | None = None


class SavingEntryOut(BaseModel):
    id: int
    budget_id: int
    name: str
    projected: float
    actual: float
    order: int

    @computed_field
    @property
    def difference(self) -> float:
        return self.actual - self.projected

    model_config = {"from_attributes": True}
