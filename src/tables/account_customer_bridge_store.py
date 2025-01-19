from __future__ import annotations

import dataclasses
from typing import overload

from src.model import DatabaseCursor


@dataclasses.dataclass
class AccountCustomerBridgeResource:
    account_id: int
    customer_id: int

    @classmethod
    def from_result_set(
        cls,
        result_set: tuple,
    ) -> AccountCustomerBridgeResource:
        if result_set:
            return AccountCustomerBridgeResource(
                account_id=result_set[0],
                customer_id=result_set[1],
            )
        raise IndexError("Account-customer bridge not found")


class AccountCustomerBridgeStore:
    def __init__(self, db_cursor: DatabaseCursor):
        self.db_cursor = db_cursor

    def create(
        self,
        data: AccountCustomerBridgeResource,
    ) -> AccountCustomerBridgeResource:
        self.db_cursor.execute(
            """
            insert into domain.account_customer_bridge(account_id, customer_id)
            values (%(account_id)s, %(customer_id)s)
            on conflict (account_id, customer_id)
            do update set deleted = false
            returning account_id, customer_id
            """,
            {
                "account_id": data.account_id,
                "customer_id": data.customer_id,
            },
        )
        return AccountCustomerBridgeResource(*self.db_cursor.fetchone())

    @overload
    def read(self, account_id: int) -> list[AccountCustomerBridgeResource]: ...

    @overload
    def read(self, customer_id: int) -> list[AccountCustomerBridgeResource]: ...

    @overload
    def read(
        self,
        account_id: int,
        customer_id: int,
    ) -> AccountCustomerBridgeResource: ...

    def read(
        self,
        account_id: int | None = None,
        customer_id: int | None = None,
    ) -> AccountCustomerBridgeResource | list[AccountCustomerBridgeResource]:
        if not account_id and not customer_id:
            raise ValueError(
                "At least one of account_id or customer_id must be provided"
            )

        if account_id and customer_id:
            self.db_cursor.execute(
                """
                select account_id, customer_id
                from domain.account_customer_bridge
                where account_id = %(account_id)s
                  and customer_id = %(customer_id)s
                  and not deleted
                """,
                {
                    "account_id": account_id,
                    "customer_id": customer_id,
                },
            )
            return AccountCustomerBridgeResource.from_result_set(
                self.db_cursor.fetchone(),
            )

        if account_id:
            self.db_cursor.execute(
                """
                select account_id, customer_id
                from domain.account_customer_bridge
                where account_id = %(account_id)s
                  and not deleted
                """,
                {"account_id": account_id},
            )
        elif customer_id:
            self.db_cursor.execute(
                """
                select account_id, customer_id
                from domain.account_customer_bridge
                where customer_id = %(customer_id)s
                  and not deleted
                """,
                {"customer_id": customer_id},
            )

        return [
            AccountCustomerBridgeResource.from_result_set(result_set)
            for result_set in self.db_cursor.fetchall()
        ]

    def update(self) -> None:
        raise NotImplementedError(
            "Update not implemented by design: account-customer bridge has no mutable public attributes"
        )

    def delete(self, identifier: AccountCustomerBridgeResource) -> None:
        self.db_cursor.execute(
            """
            update domain.account_customer_bridge
            set deleted = true
            where (account_id, customer_id) = (%(account_id)s, %(customer_id)s)
            """,
            {
                "account_id": identifier.account_id,
                "customer_id": identifier.customer_id,
            },
        )
