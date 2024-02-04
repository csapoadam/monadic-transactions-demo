from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List
from returns.maybe import Maybe, Some, Nothing ## pip install returns
from returns.pipeline import flow
from returns.pointfree import bind


@dataclass(frozen=True)
class Account:
    account_no: int
    owner: str
    balance: int

## stubbed data for now...
ACCOUNTS = {
    13542: [Account(13542, "John Doe", 35000)],
    18832: [Account(18832, "Mary Day", 42000)]
}

## All getters and sanity-check related functions should return a Maybe[Account]
def get_account(account_no: int) -> Maybe[Account]:
    ## use stub for now...
    acc_history = ACCOUNTS.get(account_no)
    if acc_history is not None:
        return Some(acc_history[len(acc_history) - 1])
    return Nothing

def account_if_has_funds(account: Account, amount: int) -> Maybe[Account]:
    if account.balance >= amount:
        return Some(account)
    return Nothing

def commit_account_update(new_account: Account, transaction: 'Transaction') -> None:
    ACCOUNTS[new_account.account_no].append(new_account)
    print(transaction)
    print(f"\t{ACCOUNTS[new_account.account_no][len(ACCOUNTS[new_account.account_no])-2]} -> ")
    print(f"\t{new_account}")

def debit_account(account: Account, amount: int) -> Account:
    return Account(account.account_no, account.owner, account.balance - amount)

def credit_account(account: Account, amount: int) -> Account:
    return Account(account.account_no, account.owner, account.balance + amount)


class Transaction(ABC):
    @abstractmethod
    def try_execute(self) -> List[Maybe[Account]]:
        pass


@dataclass(frozen=True)
class Debit(Transaction):
    account_no: int
    amount: int

    def try_execute(self) -> List[Maybe[Account]]:
        result: Maybe[Account] = flow(
            get_account(self.account_no),
            bind(lambda acc: account_if_has_funds(acc, self.amount)),
            bind(lambda acc: Maybe.from_value(debit_account(acc, self.amount))),
        )

        result.bind(lambda acc: commit_account_update(acc, self))
        return [result]    


@dataclass(frozen=True)
class Transfer(Transaction):
    source_account_no: int
    dest_account_no: int
    amount: int

    def try_execute(self) -> List[Maybe[Account]]:
        source_account: Maybe[Account] = get_account(self.source_account_no)\
            .bind(lambda sa: account_if_has_funds(sa, self.amount))\
            .value_or(None)
        dest_account: Maybe[Account] = get_account(self.dest_account_no)\
            .value_or(None)

        if source_account and dest_account:
            new_source_account = debit_account(source_account, self.amount)
            new_dest_account = credit_account(dest_account, self.amount)
            commit_account_update(new_source_account, self)
            commit_account_update(new_dest_account, self)
            return [Some(new_source_account), Some(new_dest_account)]
        return []


transactions = [
    Debit(13542, 10000),
    Debit(11111, 80000), # non-existent account
    Debit(18832, 50000), # insufficient funds
    Transfer(13542, 18832, 1500),
    Transfer(11111, 18832, 200),
    Transfer(18832, 11111, 200)
]

for tr in transactions:
    new_accounts : List[Maybe[Account]] = tr.try_execute()


