from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Budget(Base):
    __tablename__ = "budgets"
    __table_args__ = (UniqueConstraint("user_id", "month", "year", name="uq_user_month_year"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)  # 1–12
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    label: Mapped[str | None] = mapped_column(String(100))       # e.g. "May 2026"
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="budgets")
    income_entries: Mapped[list["IncomeEntry"]] = relationship(back_populates="budget", cascade="all, delete-orphan", order_by="IncomeEntry.order")
    saving_entries: Mapped[list["SavingEntry"]] = relationship(back_populates="budget", cascade="all, delete-orphan", order_by="SavingEntry.order")
    expense_categories: Mapped[list["ExpenseCategory"]] = relationship(back_populates="budget", cascade="all, delete-orphan", order_by="ExpenseCategory.order")
