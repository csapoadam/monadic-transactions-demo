from dataclasses import dataclass
from returns.maybe import Maybe, Some, Nothing

@dataclass(frozen=True)
class Account:
    account_no: int
    owner: str
    balance: int

## All getters and sanity-check related functions should return a Maybe[Account]
def account_if_has_funds(account: Account, amount: int) -> Maybe[Account]:
    if account.balance >= amount:
        return Some(account)
    return Nothing

def debit_account(account: Account, amount: int) -> Account:
    return Account(account.account_no, account.owner, account.balance - amount)

def credit_account(account: Account, amount: int) -> Account:
    return Account(account.account_no, account.owner, account.balance + amount)