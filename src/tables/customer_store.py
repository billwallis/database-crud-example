from __future__ import annotations

import dataclasses
import datetime

from src.model import DatabaseCursor


@dataclasses.dataclass
class CustomerCreationData:
    forename: str
    surname: str
    date_of_birth: datetime.date
    postcode: str


@dataclasses.dataclass
class CustomerResource:
    customer_id: int
    forename: str
    surname: str
    date_of_birth: datetime.date
    postcode: str

    @classmethod
    def from_result_set(cls, result_set: tuple) -> CustomerResource:
        if result_set:
            return CustomerResource(
                customer_id=result_set[0],
                forename=result_set[1],
                surname=result_set[2],
                date_of_birth=result_set[3],
                postcode=result_set[4],
            )
        raise IndexError("Customer not found")


class CustomerStore:
    def __init__(self, db_cursor: DatabaseCursor):
        self.db_cursor = db_cursor

    def create(self, data: CustomerCreationData) -> CustomerResource:
        self.db_cursor.execute(
            """
            insert into domain.customers(forename, surname, date_of_birth, postcode)
            values (%(forename)s, %(surname)s, %(date_of_birth)s, %(postcode)s)
            returning customer_id, forename, surname, date_of_birth, postcode
            """,
            {
                "forename": data.forename,
                "surname": data.surname,
                "date_of_birth": data.date_of_birth,
                "postcode": data.postcode,
            },
        )
        return CustomerResource(*self.db_cursor.fetchone())

    def read(self, customer_id: int) -> CustomerResource:
        self.db_cursor.execute(
            """
            select customer_id, forename, surname, date_of_birth, postcode
            from domain.customers
            where customer_id = %(customer_id)s
              and not deleted
            """,
            {"customer_id": customer_id},
        )
        return CustomerResource.from_result_set(self.db_cursor.fetchone())

    def update(self, resource: CustomerResource) -> None:
        self.db_cursor.execute(
            """
            update domain.customers
            set forename = %(forename)s,
                surname = %(surname)s,
                date_of_birth = %(date_of_birth)s,
                postcode = %(postcode)s
            where customer_id = %(customer_id)s
            """,
            {
                "customer_id": resource.customer_id,
                "forename": resource.forename,
                "surname": resource.surname,
                "date_of_birth": resource.date_of_birth,
                "postcode": resource.postcode,
            },
        )

    def delete(self, customer_id: int) -> None:
        self.db_cursor.execute(
            """
            update domain.customers
            set deleted = true
            where customer_id = %(customer_id)s
            """,
            {"customer_id": customer_id},
        )
