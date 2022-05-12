import enum
from abc import abstractmethod, ABC
from datetime import datetime
from typing import Optional

import banks.entities
import banks.utils
from banks.core import Transaction


class AccountType(enum.Enum):
    Debit = 0
    Credit = 1
    Deposit = 2
    Utility = 3


class Account(ABC):
    def __init__(self, bank: 'banks.entities.Bank', owner: Optional['banks.entities.Client']):
        self.account_id = banks.utils.get_unique_id()
        self.bank = bank
        self.owner = owner
        self.balance = 0
        self.last_updated = datetime.now()

    def add_money(self, amount: int) -> bool:
        self.balance += amount
        return True

    def subtract_money(self, amount: int, forced: bool) -> bool:
        if forced:
            self.balance -= amount
        else:
            if self.balance >= amount:
                self.balance -= amount
                return True
            else:
                return False

    @abstractmethod
    def recalculate_day(self) -> Optional[Transaction]:
        ...


class DepositAccount(Account):
    def __init__(self, bank: 'banks.entities.Bank', owner: Optional['banks.entities.Client']):
        super().__init__(bank, owner)
        self.rate = 0
        self.account_type = AccountType.Deposit
        self.opened = False

    def subtract_money(self, amount: int, forced: bool) -> bool:
        if forced:
            self.balance -= amount
            return True
        else:
            if not self.opened:
                if self.balance >= amount:
                    self.balance -= amount
                    return True
            return False

    def recalculate_day(self) -> Optional[Transaction]:
        if self.opened is None:
            return None
        added_money = int(self.rate / 365 * self.balance)
        return Transaction(added_money, self.bank.bank_id, self.bank.bank_id, self.bank.bank_account.account_id,
                           self.account_id)


class CreditAccount(Account):
    def __init__(self, bank: 'banks.entities.Bank', owner: Optional['banks.entities.Client'], fee: int,
                 limit: int):
        super().__init__(bank, owner)
        self.fee = fee
        self.limit = limit
        self.account_type = AccountType.Credit

    def subtract_money(self, amount: int, forced: bool) -> bool:
        if forced:
            self.balance -= amount
            return True
        else:
            if self.balance + self.limit >= amount:
                self.balance -= amount
                return True
            else:
                return False

    def recalculate_day(self) -> Optional[Transaction]:
        if self.balance < 0:
            return Transaction(self.fee, self.bank.bank_id, self.bank.bank_id, self.account_id,
                               self.bank.bank_account.account_id,
                               forced=True)


class DebitAccount(Account):
    def __init__(self, bank: 'banks.entities.Bank', owner: Optional['banks.entities.Client'],
                 rate: float):
        super().__init__(bank, owner)
        self.rate = rate
        self.account_type = AccountType.Debit

    def recalculate_day(self) -> Optional[Transaction]:
        added_money = int(self.rate / 365 * self.balance)
        return Transaction(added_money, self.bank.bank_id, self.bank.bank_id, self.bank.bank_account.account_id,
                           self.account_id)


class UtilityAccount(Account):
    def __init__(self, bank: 'banks.entities.Bank'):
        super().__init__(bank, None)
        self.account_type = AccountType.Utility

    def recalculate_day(self) -> Optional[Transaction]:
        return None

    def subtract_money(self, amount: int, forced: bool) -> bool:
        self.balance -= amount
        return True
