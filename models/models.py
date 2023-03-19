from typing import List

from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login = Column(String(50), unique=True)
    registration_date = Column(Date)

    credits: Mapped[List["Credit"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"user_id(id={self.id}, login={self.login}, registration_date={self.registration_date})"


class Dictionary(Base):
    __tablename__ = "dictionary"

    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column(String(50), unique=True)

    plans: Mapped[List["Plan"]] = relationship(back_populates="category")
    payments: Mapped[List["Payment"]] = relationship(back_populates="type")

    def __repr__(self) -> str:
        return f"id={self.id}, name={self.name})"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    sum = Column(Numeric(precision=19, scale=4))
    payment_date = Column(Date)
    credit_id: Mapped[int] = mapped_column(ForeignKey("credits.id"))
    type_id: Mapped[int] = mapped_column(ForeignKey("dictionary.id"))


    credit: Mapped["Credit"] = relationship(back_populates="payments")
    type: Mapped["Dictionary"] = relationship(back_populates="payments")


    def __repr__(self) -> str:
        return f"Payment(id={self.id}, name={self.sum})"


class Credit(Base):
    __tablename__ = "credits"

    id = Column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    issuance_date = Column(Date)
    return_date = Column(Date)
    actual_return_date = Column(Date)
    body = Column(Numeric(precision=19, scale=4))
    percent = Column(Numeric(precision=19, scale=4))

    user: Mapped["User"] = relationship(back_populates="credits")
    payments: Mapped[List["Payment"]] = relationship(back_populates="credit")

    def __repr__(self) -> str:
        return f"Credit(id={self.id}, body={self.body}, percent={self.percent})"


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    period = Column(Date)
    sum = Column(Numeric(precision=19, scale=4))
    category_id: Mapped[int] = mapped_column(ForeignKey("dictionary.id"))

    category: Mapped["Dictionary"] = relationship(back_populates="plans")

    def __repr__(self) -> str:
        return f"Plan(id={self.id}, sum={self.sum})"
