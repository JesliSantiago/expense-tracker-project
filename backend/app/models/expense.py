from sqlalchemy import String, Float, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class ExpenseCategory(Base):
    """A named group of expense items, e.g. 'FIXED EXPENSES', 'HOME', 'TRANSPORTATION'."""
    __tablename__ = "expense_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    budget_id: Mapped[int] = mapped_column(ForeignKey("budgets.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(150))
    order: Mapped[int] = mapped_column(Integer, default=0)

    budget: Mapped["Budget"] = relationship(back_populates="expense_categories")
    items: Mapped[list["ExpenseItem"]] = relationship(back_populates="category", cascade="all, delete-orphan", order_by="ExpenseItem.order")


class ExpenseItem(Base):
    """A single expense line within a category, e.g. 'Rent', 'Gym Membership'."""
    __tablename__ = "expense_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("expense_categories.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(150))
    projected: Mapped[float] = mapped_column(Float, default=0.0)
    actual: Mapped[float] = mapped_column(Float, default=0.0)
    order: Mapped[int] = mapped_column(Integer, default=0)

    category: Mapped["ExpenseCategory"] = relationship(back_populates="items")

    @property
    def difference(self) -> float:
        return self.actual - self.projected
