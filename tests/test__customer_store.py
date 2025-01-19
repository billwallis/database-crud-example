import copy
import datetime

import pytest

from src import (
    CustomerCreationData,
    CustomerResource,
    CustomerStore,
)


def test__customers_can_be_created(customer_store: CustomerStore):
    customer_create_data = CustomerCreationData(
        forename="Charlie",
        surname="Carter",
        date_of_birth=datetime.date(1960, 3, 3),
        postcode="IJ5 6KL",
    )
    customer_resource = CustomerResource(
        customer_id=3,
        forename="Charlie",
        surname="Carter",
        date_of_birth=datetime.date(1960, 3, 3),
        postcode="IJ5 6KL",
    )

    customer = customer_store.create(customer_create_data)
    assert customer == customer_resource


def test__customers_can_be_retrieved(
    customer_store: CustomerStore,
    customer_1: CustomerResource,
    customer_2: CustomerResource,
):
    assert customer_1 == customer_store.read(1)
    assert customer_2 == customer_store.read(2)


def test__customers_can_be_updated(
    customer_store: CustomerStore,
    customer_1: CustomerResource,
    customer_2: CustomerResource,
):
    customer_1_updated = copy.copy(customer_1)
    customer_1_updated.forename = "Alexandra"

    customer_2_updated = copy.copy(customer_2)
    customer_2_updated.forename = "Blakeley"
    customer_2_updated.date_of_birth = datetime.date(2000, 2, 2)

    customer_store.update(customer_1_updated)
    customer_store.update(customer_2_updated)

    assert customer_store.read(1) == customer_1_updated
    assert customer_store.read(2) == customer_2_updated


def test__customers_can_be_deleted(
    customer_store: CustomerStore,
    customer_1: CustomerResource,
    customer_2: CustomerResource,
):
    customer_store.delete(customer_1.customer_id)
    with pytest.raises(IndexError):
        customer_store.read(customer_1.customer_id)

    customer_store.delete(customer_2.customer_id)
    with pytest.raises(IndexError):
        customer_store.read(customer_2.customer_id)
