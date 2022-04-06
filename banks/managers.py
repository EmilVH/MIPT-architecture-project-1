from datetime import date

from banks.core import Transaction


class BankManager:
    def __init__(self):
        self.all_banks = None
        self.transaction_history = None
        self.recalculation_manager = None

    def execute_transaction(self, transaction: Transaction):
        pass

    def rollback_transaction(self, transaction: Transaction):
        pass


class RecalculationManager:
    def __init__(self):
        self.bank_manager = None
        self.current_date = None

    def skip_to_date(self, to_date: date):
        pass