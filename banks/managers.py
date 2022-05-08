from datetime import date, datetime, timedelta
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
    def __init__(self, bank_manager: BankManager):
        self.bank_manager = bank_manager
        self.time_controller = TimeController()

    def next_day(self):
        prev_time = self.time_controller.get_curr_time()
        recal_time = datetime(year=prev_time.year, month=prev_time.month, day=prev_time.day, hour=23, minute=59,
                              second=59)
        self.time_controller.set_time(recal_time)
        self.bank_manager.start_day_recalculation()
        self.time_controller.set_time(prev_time + timedelta(days=1))

    def prev_day(self):
        prev_time = self.time_controller.get_curr_time()
        new_time = prev_time - timedelta(days=1)
        self.bank_manager.start_day_recalculation()
        self.time_controller.set_time(prev_time - timedelta(days=1))
    def skip_to_date(self, to_date: date):
        pass
