from __future__ import annotations

import dataclasses

from src.model import DatabaseCursor


@dataclasses.dataclass
class AccountResource:
    account_id: int

    @classmethod
    def from_result_set(cls, result_set: tuple) -> AccountResource:
        if result_set:
            return AccountResource(account_id=result_set[0])
        raise IndexError("Account not found")


class AccountStore:
    def __init__(self, db_cursor: DatabaseCursor):
        self.db_cursor = db_cursor

    def create(self) -> AccountResource:
        self.db_cursor.execute(
            """
            insert into domain.accounts
            default values
            returning account_id
            """
        )
        return AccountResource.from_result_set(self.db_cursor.fetchone())

    def read(self, account_id: int) -> AccountResource:
        self.db_cursor.execute(
            """
            select account_id
            from domain.accounts
            where account_id = %(account_id)s
              and not deleted
            """,
            {"account_id": account_id},
        )
        return AccountResource.from_result_set(self.db_cursor.fetchone())

    def update(self) -> None:
        raise NotImplementedError(
            "Update not implemented by design: account has no mutable public attributes"
        )

    def delete(self, account_id: int) -> None:
        self.db_cursor.execute(
            """
            update domain.accounts
            set deleted = true
            where account_id = %(account_id)s
            """,
            {"account_id": account_id},
        )
