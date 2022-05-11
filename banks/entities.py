from typing import List, Optional, Dict

import banks.accounts
import banks.core
import banks.utils


class Client:
    def __init__(self, name: str, surname: str, address: Optional['banks.utils.Address'] = None,
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

    def __str__(self) -> str:
        return self.name_to_str(self.name.lower(), self.surname.lower())

    # def __eq__(self, other):
    #     return self.__hash__() == other.__hash__()
    @staticmethod
    def name_to_str(name: str, surname: str) -> str:
        return name.lower() + ' ' + surname.lower()


class Bank:
    def __init__(self, name: str, credit_fee: int = 100, credit_limit: int = 10000, debit_rate: float = 0.1,
                 deposit_rates: Dict[int, float] = {1000: 0.1, 10000: 0.15, 100000: 0.2}):
        self.name = name
        self.bank_id = banks.utils.get_unique_id()
        self.all_accounts: Dict[int, 'banks.accounts.Account'] = dict()
        self.all_clients: Dict[str, Client] = dict()
        self.clients_accounts: Dict[Optional[str], Optional[List['banks.accounts.Account']]] = dict()
        self.default_credit_limit = credit_limit
        self.default_credit_fee = credit_fee
        self.default_debit_rate = debit_rate
        self.default_deposit_rates = deposit_rates
        # self.atms: Dict[int, banks.utils.ATM] = dict()
        self.unique_id_generator = banks.utils.UniqueIdGeneratorSingleton()
        # self.bank_manager = None
        self.bank_account = banks.accounts.UtilityAccount(self)
        # self.cash_account = bank .accounts.UtilityAccount(self.unique_id_generator.generate_new_unique_id(), self)
        self.all_accounts[self.bank_account.account_id] = self.bank_account
        # self.all_accounts[self.cash_account.account_id] = self.`
        self.clients_accounts[None] = list()
        self.clients_accounts[None].append(self.bank_account)
        # self.clients_accounts[None].append(self.cash_account)

    def get_account(self, account_id: int) -> Optional['banks.accounts.Account']:
        if account_id in self.all_accounts:
            return self.all_accounts[account_id]

    def add_account(self, client: Client, account_type: int) -> Optional['banks.accounts.Account']:
        new_account = None
        if account_type == banks.accounts.AccountType.Debit:
            new_account = banks.accounts.DebitAccount(self, client, self.default_debit_rate)
        if account_type == banks.accounts.AccountType.Credit:
            new_account = banks.accounts.CreditAccount(self, client, self.default_credit_fee, self.default_credit_limit)
        if account_type == banks.accounts.AccountType.Deposit:
            new_account = banks.accounts.DepositAccount(self, client)
        self.clients_accounts[str(client)].append(new_account)
        self.all_accounts[new_account.account_id] = new_account
        return new_account

    def deposit_open(self, deposit_account: 'banks.accounts.DepositAccount', account_from: 'banks.accounts.Account',
                     amount: int) -> bool:
        # open_transaction = banks.core.Transaction(amount, self.bank_id, self.bank_id, account_from.account_id,
        #                                           debit_account.account_id)
        if deposit_account.account_id not in self.all_accounts:
            return False
        if deposit_account.opened:
            return False
        if account_from.account_id not in self.all_accounts:
            return False
        max_rate = 0
        for needed_amount, val in self.default_deposit_rates.items():
            if amount >= needed_amount:
                max_rate = max(val, max_rate)
        deposit_account.balance = amount
        deposit_account.rate = max_rate
        account_from.balance -= amount
        deposit_account.opened = True
        return True

    def deposit_close(self, deposit_account: 'banks.accounts.DepositAccount',
                      account_to: 'banks.accounts.Account') -> bool:
        # open_transaction = banks.core.Transaction(amount, self.bank_id, self.bank_id, account_from.account_id,
        #                                           debit_account.account_id)
        if deposit_account.account_id not in self.all_accounts:
            return False
        if not deposit_account.opened:
            return False
        if account_to not in self.all_accounts:
            return False
        account_to += deposit_account.balance
        deposit_account.balance = 0
        deposit_account.opened = False

    def add_client(self, client: Client):
        if str(client) in self.all_clients:
            return
        self.clients_accounts[str(client)] = list()
        self.all_clients[str(client)] = client

    def search_client(self, name: str, surname: str) -> Optional[Client]:
        find_str = Client.name_to_str(name, surname)
        if find_str in self.all_clients:
            return self.all_clients[find_str]

    def recalculate_day(self) -> List['banks.core.Transaction']:
        ans = list()
        for account_id, account in self.all_accounts.items():
            res = account.recalculate_day()
            if res is not None:
                ans.append(res)
        return ans
