from sqlalchemy import String, Float, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class SavingEntry(Base):
    __tablename__ = "saving_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    budget_id: Mapped[int] = mapped_column(ForeignKey("budgets.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(150))       # e.g. "Emergency Fund", "MP2"
    projected: Mapped[float] = mapped_column(Float, default=0.0)
    actual: Mapped[float] = mapped_column(Float, default=0.0)
    order: Mapped[int] = mapped_column(Integer, default=0)

    budget: Mapped["Budget"] = relationship(back_populates="saving_entries")

    @property
    def difference(self) -> float:
        return self.actual - self.projected
