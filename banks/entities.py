from typing import List

from banks.accounts import Account
from banks.core import Transaction


class Client:
    def __init__(self):
        self.name = None
        self.surname = None
        self.address = None
        self.id_number = None
        self.is_verified = None

    def try_verify(self):
        pass


class Bank:
    def __init__(self):
        self.name = None
        self.id = None
        self.all_clients = None
        self.all_accounts = None
        self.bank_manager = None
        self.bank_account = None
        self.cash_account = None
        self.atms = None

    def get_account(self, account_id: int) -> Account:
        pass

    def add_client(self, client: Client):
        pass

    def search_client(self) -> Client:
        pass

    def recalculate_day(self) -> List[Transaction]:
        pass
