from abc import abstractmethod, ABC
from datetime import datetime
from typing import Optional

import banks.entities
from banks.core import Transaction


class Account(ABC):
    def __init__(self, account_id: int, bank: 'banks.entities.Bank', owner: Optional['banks.entities.Client']):
        self.account_id = account_id
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
    def __init__(self, account_id: int, bank: 'banks.entities.Bank', rate: float):
        super().__init__(account_id, bank, 1)
        self.rate = rate

    def subtract_money(self, amount: int, forced: bool) -> bool:
        return False

    def recalculate_day(self) -> Optional[Transaction]:
        added_money = int(self.rate / 365 * self.balance)
        return Transaction(added_money, self.bank.id, self.bank.id, self.bank.bank_account, self.account_id)


class CreditAccount(Account):
    def __init__(self, account_id: int, bank: 'banks.entities.Bank', owner: Optional['banks.entities.Client'], fee: int,
                 limit: int):
        super().__init__(account_id, bank, owner)
        self.fee = fee
        self.limit = limit

    def subtract_money(self, amount: int, forced: bool) -> bool:
        if forced:
            self.balance -= amount
        else:
            if self.balance + self.limit >= amount:
                self.balance -= amount
                return True
            else:
                return False

    def recalculate_day(self) -> Optional[Transaction]:
        if self.balance < 0:
            return Transaction(self.fee, self.bank.id, self.bank.id, self.account_id, self.bank.bank_account,
                               forced=True)


class DebitAccount(Account):
    def __init__(self, account_id: int, bank: 'banks.entities.Bank', owner: Optional['banks.entities.Client'],
                 rate: float):
        super().__init__(account_id, bank, owner)
        self.rate = rate

    def recalculate_day(self) -> Optional[Transaction]:
        added_money = int(self.rate / 365 * self.balance)
        return Transaction(added_money, self.bank.id, self.bank.id, self.bank.bank_account, self.account_id)


class UtilityAccount(Account):
    def __init__(self, account_id: int, bank: 'banks.entities.Bank'):
        super().__init__(account_id, bank, None)

    def recalculate_day(self) -> Optional[Transaction]:
        return None

    def subtract_money(self, amount: int, forced: bool) -> bool:
        self.balance -= amount
