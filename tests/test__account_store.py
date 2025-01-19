import pytest

from src import (
    AccountResource,
    AccountStore,
)


def test__accounts_can_be_created(account_store: AccountStore):
    account_3 = account_store.create()
    assert account_3 == AccountResource(account_id=3)


def test__accounts_can_be_retrieved(
    account_store: AccountStore,
    account_1: AccountResource,
    account_2: AccountResource,
):
    assert account_1 == account_store.read(1)
    assert account_2 == account_store.read(2)


def test__accounts_cannot_be_updated(account_store: AccountStore):
    with pytest.raises(NotImplementedError):
        account_store.update()


def test__accounts_can_be_deleted(
    account_store: AccountStore,
    account_1: AccountResource,
    account_2: AccountResource,
):
    account_store.delete(account_1.account_id)
    with pytest.raises(IndexError):
        account_store.read(account_1.account_id)

    account_store.delete(account_2.account_id)
    with pytest.raises(IndexError):
        account_store.read(account_2.account_id)
