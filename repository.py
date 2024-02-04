from account import Account
from returns.maybe import Maybe
from abc import ABC, abstractmethod


class Repository(ABC):
    ## All getters and sanity-check related functions should return a Maybe[Account]
    @abstractmethod
    def get_account(self, account_no: int) -> Maybe[Account]:
        pass

    @abstractmethod
    def commit_account_update(self, new_account: Account) -> None:
        pass