from abc import ABC, abstractmethod
from dataclasses import dataclass
from returns.maybe import Maybe, Some
from returns.pointfree import bind
from returns.pipeline import flow
from typing import List
from account import Account, account_if_has_funds, credit_account, debit_account
from repository import Repository

class Transaction(ABC):
    @abstractmethod
    def try_execute(self, repo: Repository) -> List[Maybe[Account]]:
        pass


@dataclass(frozen=True)
class Debit(Transaction):
    account_no: int
    amount: int

    def try_execute(self, repo: Repository) -> List[Maybe[Account]]:
        result: Maybe[Account] = flow(
            repo.get_account(self.account_no),
            bind(lambda acc: account_if_has_funds(acc, self.amount)),
            bind(lambda acc: Maybe.from_value(debit_account(acc, self.amount))),
        )

        result.bind(repo.commit_account_update)
        return [result]


@dataclass(frozen=True)
class Transfer(Transaction):
    source_account_no: int
    dest_account_no: int
    amount: int

    def try_execute(self, repo: Repository) -> List[Maybe[Account]]:
        source_account: Maybe[Account] = repo.get_account(self.source_account_no)\
            .bind(lambda sa: account_if_has_funds(sa, self.amount))\
            .value_or(None)
        dest_account: Maybe[Account] = repo.get_account(self.dest_account_no)\
            .value_or(None)

        if source_account and dest_account:
            new_source_account = debit_account(source_account, self.amount)
            new_dest_account = credit_account(dest_account, self.amount)
            repo.commit_account_update(new_source_account)
            repo.commit_account_update(new_dest_account)
            return [Some(new_source_account), Some(new_dest_account)]
        return []
