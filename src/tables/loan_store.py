from __future__ import annotations

import dataclasses
import datetime
import decimal
import math

from src.model import DatabaseCursor


@dataclasses.dataclass
class LoanCreationData:
    account_id: int
    amount: decimal.Decimal
    interest_rate: decimal.Decimal
    start_date: datetime.date
    end_date: datetime.date
    current_balance: decimal.Decimal


@dataclasses.dataclass
class LoanResource:
    loan_id: int
    account_id: int
    amount: decimal.Decimal
    interest_rate: decimal.Decimal
    start_date: datetime.date
    end_date: datetime.date
    current_balance: decimal.Decimal

    def __eq__(self, other: LoanResource):
        return (
            self.loan_id == other.loan_id
            and self.account_id == other.account_id
            and math.isclose(self.amount, other.amount)
            and math.isclose(self.interest_rate, other.interest_rate)
            and self.start_date == other.start_date
            and self.end_date == other.end_date
            and math.isclose(self.current_balance, other.current_balance)
        )

    @classmethod
    def from_result_set(cls, result_set: tuple) -> LoanResource:
        if result_set:
            return LoanResource(
                loan_id=result_set[0],
                account_id=result_set[1],
                amount=result_set[2],
                interest_rate=result_set[3],
                start_date=result_set[4],
                end_date=result_set[5],
                current_balance=result_set[6],
            )
        raise IndexError("Loan not found")


class LoanStore:
    def __init__(self, db_cursor: DatabaseCursor):
        self.db_cursor = db_cursor

    def create(self, data: LoanCreationData) -> LoanResource:
        self.db_cursor.execute(
            """
            insert into domain.loans(account_id, amount, interest_rate, start_date, end_date, current_balance)
            values (%(account_id)s, %(amount)s, %(interest_rate)s, %(start_date)s, %(end_date)s, %(current_balance)s)
            returning loan_id, account_id, amount, interest_rate, start_date, end_date, current_balance
            """,
            {
                "account_id": data.account_id,
                "amount": data.amount,
                "interest_rate": data.interest_rate,
                "start_date": data.start_date,
                "end_date": data.end_date,
                "current_balance": data.current_balance,
            },
        )
        return LoanResource(*self.db_cursor.fetchone())

    def read(self, loan_id: int) -> LoanResource:
        self.db_cursor.execute(
            """
            select loan_id, account_id, amount, interest_rate, start_date, end_date, current_balance
            from domain.loans
            where loan_id = %(loan_id)s
              and not deleted
            """,
            {"loan_id": loan_id},
        )
        return LoanResource.from_result_set(self.db_cursor.fetchone())

    def update(self, resource: LoanResource) -> None:
        self.db_cursor.execute(
            """
            update domain.loans
            set account_id = %(account_id)s,
                amount = %(amount)s,
                interest_rate = %(interest_rate)s,
                start_date = %(start_date)s,
                end_date = %(end_date)s,
                current_balance = %(current_balance)s
            where loan_id = %(loan_id)s
            """,
            {
                "loan_id": resource.loan_id,
                "account_id": resource.account_id,
                "amount": resource.amount,
                "interest_rate": resource.interest_rate,
                "start_date": resource.start_date,
                "end_date": resource.end_date,
                "current_balance": resource.current_balance,
            },
        )

    def delete(self, loan_id: int) -> None:
        self.db_cursor.execute(
            """
            update domain.loans
            set deleted = true
            where loan_id = %(loan_id)s
            """,
            {"loan_id": loan_id},
        )
