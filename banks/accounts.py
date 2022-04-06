from abc import abstractmethod, ABC

from banks.core import Transaction


class Account(ABC):
    @abstractmethod
    def add_money(self, amount: int) -> bool:
        pass

    @abstractmethod
    def subtract_money(self, amount: int) -> bool:
        pass

    @abstractmethod
    def recalculate_day(self) -> Transaction:
        pass


class DepositAccount(Account):
    pass


class CreditAccount(Account):
    pass


class DebitAccount(Account):
    pass


class UtilityAccount(Account):
    pass
