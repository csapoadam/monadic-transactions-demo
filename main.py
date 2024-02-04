from typing import List
from returns.maybe import Maybe

from repository import Repository
from repository_stub import RepositoryStub
from transaction import Debit, Transfer
from account import Account


if __name__ == "__main__":
    repository: Repository = RepositoryStub()

    transactions = [
        Debit(13542, 10000),
        Debit(11111, 80000), # non-existent account
        Debit(18832, 50000), # insufficient funds
        Transfer(13542, 18832, 1500),
        Transfer(11111, 18832, 200), # no such source account
        Transfer(18832, 11111, 200) # no such dest account
    ]

    for tr in transactions:
        new_accounts : List[Maybe[Account]] = tr.try_execute(repository)


