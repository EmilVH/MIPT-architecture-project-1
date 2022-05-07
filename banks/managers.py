from datetime import date
from typing import List, Dict

import banks.entities
from banks.core import Transaction
from banks.time_controller import TimeController


class BankManager:
    def __init__(self):
        self.all_banks: Dict[int, banks.entities.Bank] = dict()
        self.transaction_history: List[Transaction] = list()
        self.recalculation_manager = RecalculationManager()

    def execute_transaction(self, transaction: Transaction):
        account_from = self.all_banks[transaction.bank_from_id].get_account(transaction.account_from_id)
        account_to = self.all_banks[transaction.bank_to_id].get_account(transaction.account_to_id)
        res = account_from.subtract_money(transaction.amount, forced=transaction.forced)
        if res:
            account_to.add_money(transaction.amount)
        else:
            return False
        self.transaction_history.append(transaction)
        return True

    def rollback_transaction(self, transaction: Transaction):
        account_to = self.all_banks[transaction.bank_from_id].get_account(transaction.account_from_id)
        account_from = self.all_banks[transaction.bank_to_id].get_account(transaction.account_to_id)
        account_from.subtract_money(transaction.amount, forced=True)
        account_to.add_money(transaction.amount)
        # self.transaction_history.append(transaction)
        return True

    def start_day_recalculation(self):
        for bank_id, bank in self.all_banks.items():
            transactions = bank.recalculate_day()
            for transaction in transactions:
                self.execute_transaction(transaction)


class RecalculationManager:
    def __init__(self):
        self.bank_manager = None
        self.time_controller = TimeController()
    def next_day(self):

    def skip_to_date(self, to_date: date):
        pass
