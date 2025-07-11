import datetime
import decimal
import os
from collections.abc import Generator

import psycopg
import pytest

import src


@pytest.fixture
def db_conn() -> Generator[psycopg.Connection, None, None]:
    """
    Setup and teardown a database connection.

    This is an expensive operation, but we need separate transactions
    for each test.
    """
    # TODO: find a better approach for transaction isolation
    db_config = src.DBConfig(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", "5433")),
        database="test_db",
        user="test_db",
        password="test_db",  # noqa: S106
    )
    conn = psycopg.connect(db_config.dsn, connect_timeout=3)
    try:
        src.migrate_up(conn)
        yield conn
        src.migrate_down(conn)
    finally:
        conn.close()


@pytest.fixture
def account_1() -> src.AccountResource:
    return src.AccountResource(account_id=1)


@pytest.fixture
def account_2() -> src.AccountResource:
    return src.AccountResource(account_id=2)


@pytest.fixture
def customer_1__create_data() -> src.CustomerCreationData:
    return src.CustomerCreationData(
        forename="Alex",
        surname="Allen",
        date_of_birth=datetime.date(1990, 1, 1),
        postcode="AB1 2CD",
    )


@pytest.fixture
def customer_1() -> src.CustomerResource:
    return src.CustomerResource(
        customer_id=1,
        forename="Alex",
        surname="Allen",
        date_of_birth=datetime.date(1990, 1, 1),
        postcode="AB1 2CD",
    )


@pytest.fixture
def customer_2__create_data() -> src.CustomerCreationData:
    return src.CustomerCreationData(
        forename="Blake",
        surname="Baker",
        date_of_birth=datetime.date(1991, 2, 2),
        postcode="EF3 4GH",
    )


@pytest.fixture
def customer_2() -> src.CustomerResource:
    return src.CustomerResource(
        customer_id=2,
        forename="Blake",
        surname="Baker",
        date_of_birth=datetime.date(1991, 2, 2),
        postcode="EF3 4GH",
    )


@pytest.fixture
def loan_1__create_data() -> src.LoanCreationData:
    return src.LoanCreationData(
        account_id=1,
        amount=decimal.Decimal("1_000"),
        interest_rate=decimal.Decimal("0.15"),
        start_date=datetime.date(2020, 1, 1),
        end_date=datetime.date(2021, 1, 1),
        current_balance=decimal.Decimal("1_000"),
    )


@pytest.fixture
def loan_1() -> src.LoanResource:
    return src.LoanResource(
        loan_id=1,
        account_id=1,
        amount=decimal.Decimal("1_000"),
        interest_rate=decimal.Decimal("0.15"),
        start_date=datetime.date(2020, 1, 1),
        end_date=datetime.date(2021, 1, 1),
        current_balance=decimal.Decimal("1_000"),
    )


@pytest.fixture
def loan_2__create_data() -> src.LoanCreationData:
    return src.LoanCreationData(
        account_id=1,
        amount=decimal.Decimal("10_000"),
        interest_rate=decimal.Decimal("0.10"),
        start_date=datetime.date(2020, 2, 1),
        end_date=datetime.date(2021, 2, 1),
        current_balance=decimal.Decimal("10_000"),
    )


@pytest.fixture
def loan_2() -> src.LoanResource:
    return src.LoanResource(
        loan_id=2,
        account_id=1,
        amount=decimal.Decimal("10_000"),
        interest_rate=decimal.Decimal("0.10"),
        start_date=datetime.date(2020, 2, 1),
        end_date=datetime.date(2021, 2, 1),
        current_balance=decimal.Decimal("10_000"),
    )


@pytest.fixture
def loan_3__create_data() -> src.LoanCreationData:
    return src.LoanCreationData(
        account_id=2,
        amount=decimal.Decimal("15_000"),
        interest_rate=decimal.Decimal("0.05"),
        start_date=datetime.date(2020, 3, 1),
        end_date=datetime.date(2021, 3, 1),
        current_balance=decimal.Decimal("15_000"),
    )


@pytest.fixture
def loan_3() -> src.LoanResource:
    return src.LoanResource(
        loan_id=3,
        account_id=2,
        amount=decimal.Decimal("15_000"),
        interest_rate=decimal.Decimal("0.05"),
        start_date=datetime.date(2020, 3, 1),
        end_date=datetime.date(2021, 3, 1),
        current_balance=decimal.Decimal("15_000"),
    )


@pytest.fixture
def account_1_customer_1() -> src.AccountCustomerBridgeResource:
    return src.AccountCustomerBridgeResource(
        account_id=1,
        customer_id=1,
    )


@pytest.fixture
def account_1_customer_2() -> src.AccountCustomerBridgeResource:
    return src.AccountCustomerBridgeResource(
        account_id=1,
        customer_id=2,
    )


@pytest.fixture
def account_2_customer_2() -> src.AccountCustomerBridgeResource:
    return src.AccountCustomerBridgeResource(
        account_id=2,
        customer_id=2,
    )


@pytest.fixture
def account_store(
    db_conn: src.DatabaseConnection,
):
    return src.AccountStore(db_conn.cursor())


@pytest.fixture
def customer_store(
    db_conn: src.DatabaseConnection,
) -> src.CustomerStore:
    return src.CustomerStore(db_conn.cursor())


@pytest.fixture
def loan_store(
    db_conn: src.DatabaseConnection,
) -> src.LoanStore:
    return src.LoanStore(db_conn.cursor())


@pytest.fixture
def account_customer_store(
    db_conn: src.DatabaseConnection,
) -> src.AccountCustomerBridgeStore:
    return src.AccountCustomerBridgeStore(db_conn.cursor())


@pytest.fixture(autouse=True)
def create_database_fixtures(
    account_store: src.AccountStore,
    account_1: src.AccountResource,
    account_2: src.AccountResource,
    customer_store: src.CustomerStore,
    customer_1__create_data: src.CustomerCreationData,
    customer_2__create_data: src.CustomerCreationData,
    loan_store: src.LoanStore,
    loan_1__create_data: src.LoanCreationData,
    loan_2__create_data: src.LoanCreationData,
    loan_3__create_data: src.LoanCreationData,
    account_customer_store: src.AccountCustomerBridgeStore,
    account_1_customer_1: src.AccountCustomerBridgeResource,
    account_1_customer_2: src.AccountCustomerBridgeResource,
    account_2_customer_2: src.AccountCustomerBridgeResource,
):
    account_store.create()
    account_store.create()

    customer_store.create(customer_1__create_data)
    customer_store.create(customer_2__create_data)

    loan_store.create(loan_1__create_data)
    loan_store.create(loan_2__create_data)
    loan_store.create(loan_3__create_data)

    account_customer_store.create(account_1_customer_1)
    account_customer_store.create(account_1_customer_2)
    account_customer_store.create(account_2_customer_2)
