import pytest

from src import (
    AccountCustomerBridgeResource,
    AccountCustomerBridgeStore,
)


def test__account_customer_bridges_can_be_created(
    account_customer_store: AccountCustomerBridgeStore,
):
    account_customer_bridge = AccountCustomerBridgeResource(
        account_id=2,
        customer_id=1,
    )

    bridge = account_customer_store.create(account_customer_bridge)
    assert bridge == account_customer_bridge


@pytest.mark.parametrize(
    "identifier, expected",
    [
        (
            {"account_id": 1},
            [
                AccountCustomerBridgeResource(account_id=1, customer_id=1),
                AccountCustomerBridgeResource(account_id=1, customer_id=2),
            ],
        ),
        (
            {"customer_id": 2},
            [
                AccountCustomerBridgeResource(account_id=1, customer_id=2),
                AccountCustomerBridgeResource(account_id=2, customer_id=2),
            ],
        ),
        (
            {"account_id": 1, "customer_id": 1},
            AccountCustomerBridgeResource(account_id=1, customer_id=1),
        ),
    ],
)
def test__account_customer_bridges_can_be_retrieved(
    account_customer_store: AccountCustomerBridgeStore,
    identifier: dict[str, int],
    expected: AccountCustomerBridgeResource,
):
    assert account_customer_store.read(**identifier) == expected


def test__account_customer_bridges_cannot_be_retrieved_without_ids(
    account_customer_store: AccountCustomerBridgeStore,
):
    with pytest.raises(ValueError):
        account_customer_store.read()


def test__account_customer_bridges_cannot_be_updated(
    account_customer_store: AccountCustomerBridgeStore,
):
    with pytest.raises(NotImplementedError):
        account_customer_store.update()


def test__account_customer_bridges_can_be_deleted(
    account_customer_store: AccountCustomerBridgeStore,
    account_1_customer_1: AccountCustomerBridgeResource,
    account_1_customer_2: AccountCustomerBridgeResource,
    account_2_customer_2: AccountCustomerBridgeResource,
):
    account_customer_store.delete(account_1_customer_1)
    with pytest.raises(IndexError):
        account_customer_store.read(
            account_id=account_1_customer_1.account_id,
            customer_id=account_1_customer_1.customer_id,
        )

    account_customer_store.delete(account_1_customer_2)
    with pytest.raises(IndexError):
        account_customer_store.read(
            account_id=account_1_customer_2.account_id,
            customer_id=account_1_customer_2.customer_id,
        )

    account_customer_store.delete(account_2_customer_2)
    with pytest.raises(IndexError):
        account_customer_store.read(
            account_id=account_2_customer_2.account_id,
            customer_id=account_2_customer_2.customer_id,
        )
