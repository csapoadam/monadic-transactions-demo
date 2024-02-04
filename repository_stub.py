from repository import Repository
from account import Account
from returns.maybe import Maybe, Some, Nothing

class RepositoryStub(Repository):
    """
    Repository using stubbed data...
    """
    def __init__(self):
        self.ACCOUNTS = {
            13542: [Account(13542, "John Doe", 35000)],
            18832: [Account(18832, "Mary Day", 42000)]
        }

    ## All getters and sanity-check related functions should return a Maybe[Account]
    def get_account(self, account_no: int) -> Maybe[Account]:
        ## use stub for now...
        acc_history = self.ACCOUNTS.get(account_no)
        if acc_history is not None:
            return Some(acc_history[len(acc_history) - 1])
        return Nothing

    def commit_account_update(self, new_account: Account) -> None:
        self.ACCOUNTS[new_account.account_no].append(new_account)
        print(f"\t{self.ACCOUNTS[new_account.account_no][len(self.ACCOUNTS[new_account.account_no])-2]} -> ")
        print(f"\t{new_account}")