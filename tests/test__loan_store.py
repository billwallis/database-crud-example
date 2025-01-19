import copy
import datetime
import decimal

import pytest

from src import (
    LoanCreationData,
    LoanResource,
    LoanStore,
)


def test__loans_can_be_created(loan_store: LoanStore):
    loan_creation_data = LoanCreationData(
        account_id=2,
        amount=decimal.Decimal(20_000),
        interest_rate=decimal.Decimal(0.025),
        start_date=datetime.date(2020, 4, 1),
        end_date=datetime.date(2021, 4, 1),
        current_balance=decimal.Decimal(20_000),
    )
    loan_resource = LoanResource(
        loan_id=4,
        account_id=2,
        amount=decimal.Decimal(20_000),
        interest_rate=decimal.Decimal(0.025),
        start_date=datetime.date(2020, 4, 1),
        end_date=datetime.date(2021, 4, 1),
        current_balance=decimal.Decimal(20_000),
    )

    loan = loan_store.create(loan_creation_data)
    assert loan == loan_resource


def test__loans_can_be_retrieved(
    loan_store: LoanStore,
    loan_1: LoanResource,
    loan_2: LoanResource,
    loan_3: LoanResource,
):
    assert loan_1 == loan_store.read(1)
    assert loan_2 == loan_store.read(2)
    assert loan_3 == loan_store.read(3)


def test__loans_can_be_updated(
    loan_store: LoanStore,
    loan_1: LoanResource,
    loan_2: LoanResource,
):
    loan_1_updated = copy.copy(loan_1)
    loan_1_updated.interest_rate = decimal.Decimal(0.20)

    loan_2_updated = copy.copy(loan_2)
    loan_2_updated.interest_rate = decimal.Decimal(0.20)
    loan_2_updated.current_balance = decimal.Decimal(12_250.50)

    loan_store.update(loan_1_updated)
    loan_store.update(loan_2_updated)

    assert loan_store.read(1) == loan_1_updated
    assert loan_store.read(2) == loan_2_updated


def test__loans_can_be_deleted(
    loan_store: LoanStore,
    loan_1: LoanResource,
    loan_2: LoanResource,
):
    loan_store.delete(loan_1.loan_id)
    with pytest.raises(IndexError):
        loan_store.read(loan_1.loan_id)

    loan_store.delete(loan_2.loan_id)
    with pytest.raises(IndexError):
        loan_store.read(loan_2.loan_id)
