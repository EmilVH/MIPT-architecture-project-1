from typing import List, Optional, Dict

import banks.accounts
import banks.utils
from banks.core import Transaction


class Client:
    def __init__(self, name: str, surname: str, address: Optional[banks.utils.Address] = None,
                 id_number: Optional[int] = None):
        self.name = name.lower()
        self.surname = surname.lower()
        self.address = address
        self.id_number = id_number
        self.is_verified: Optional[bool] = None
        self.all_accounts: List[banks.accounts.Account] = list()
        self.try_verify()

    def try_verify(self):
        if self.id_number is not None and self.address is not None and self.address.validate():
            self.is_verified = True

    # def __str__(self) -> str:
    #     return self.name.lower() + ' ' + self.surname.lower()
    #
    # def __eq__(self, other):
    #     return self.__hash__() == other.__hash__()
    @staticmethod
    def name_to_str(name: str, surname: str) -> str:
        return name.lower() + ' ' + surname.lower()


class Bank:
    def __init__(self, name: str):
        self.name = name
        self.id = None
        self.all_accounts: Dict[int, banks.accounts.Account] = dict()
        self.all_clients: Dict[str, Client] = dict()
        self.atms: Dict[int, banks.utils.ATM] = dict()
        self.unique_id_generator = banks.utils.UniqueIdGeneratorSingleton()
        # self.bank_manager = None
        self.bank_account = banks.accounts.UtilityAccount(self.unique_id_generator.generate_new_unique_id(), self)
        # self.cash_account = bank .accounts.UtilityAccount(self.unique_id_generator.generate_new_unique_id(), self)
        self.all_accounts[self.bank_account.account_id] = self.bank_account
        # self.all_accounts[self.cash_account.account_id] = self.`
        # self.clients_accounts[None].append(self.bank_account)
        # self.clients_accounts[None].append(self.cash_account)

    def get_account(self, account_id: int) -> Optional[banks.accounts.Account]:
        if account_id in self.all_accounts:
            return self.all_accounts[account_id]

    def add_client(self, client: Client):
        self.all_clients[str(client)] = client

    def search_client(self, name: str, surname: str) -> Optional[Client]:
        find_str = Client.name_to_str(name, surname)
        if find_str in self.all_clients:
            return self.all_clients[find_str]

    def recalculate_day(self) -> List[Transaction]:
        ans = list()
        for account_id, account in self.all_accounts.items():
            ans.append(account.recalculate_day())
        return ans