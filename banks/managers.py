from datetime import date, datetime, timedelta
from typing import List, Dict

import banks.entities
from banks.core import Transaction, TransactionState
from banks.time_controller import TimeController, get_time


class BankManager:
    def __init__(self):
        self.all_banks: Dict[int, banks.entities.Bank] = dict()
        self.executed_transaction_history: List[Transaction] = list()
        self.cancelled_transaction_history: List[Transaction] = list()
        self.recalculation_manager = RecalculationManager(self)

    def execute_transaction(self, transaction: Transaction):
        if transaction.state is not TransactionState.UNEXECUTED:
            transaction.state = TransactionState.CANCELLED
            self.cancelled_transaction_history.append(transaction)
            return False
        account_from = self.all_banks[transaction.bank_from_id].get_account(transaction.account_from_id)
        account_to = self.all_banks[transaction.bank_to_id].get_account(transaction.account_to_id)
        if (account_from.owner is not None and not account_from.owner.is_verified) or (
                account_to.owner is not None and not account_to.owner.is_verified):
            transaction.state = TransactionState.CANCELLED
            self.cancelled_transaction_history.append(transaction)
            return False
        res = account_from.subtract_money(transaction.amount, forced=transaction.forced)
        if res:
            account_to.add_money(transaction.amount)
        else:
            transaction.state = TransactionState.CANCELLED
            self.cancelled_transaction_history.append(transaction)
            return False
        transaction.state = TransactionState.EXECUTED
        transaction.execution_time = get_time()
        self.executed_transaction_history.append(transaction)
        return True

    def create_bank(self, bank_name: str) -> banks.entities.Bank:
        new_bank = banks.entities.Bank(bank_name)
        self.all_banks[new_bank.bank_id] = new_bank
        return new_bank

    def cancel_transaction(self, transaction: Transaction):
        if transaction.state is not TransactionState.EXECUTED:
            return False
        account_to = self.all_banks[transaction.bank_from_id].get_account(transaction.account_from_id)
        account_from = self.all_banks[transaction.bank_to_id].get_account(transaction.account_to_id)
        account_from.subtract_money(transaction.amount, forced=True)
        account_to.add_money(transaction.amount)
        transaction.state = TransactionState.CANCELLED
        self.cancelled_transaction_history.append(transaction)
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
        recalc_time = datetime(year=prev_time.year, month=prev_time.month, day=prev_time.day, hour=23, minute=59,
                               second=59)
        self.time_controller.set_time(recalc_time)
        self.bank_manager.start_day_recalculation()
        self.time_controller.set_time(prev_time + timedelta(days=1))

    def prev_day(self):
        prev_time = self.time_controller.get_curr_time()
        new_time_date = (prev_time - timedelta(days=1)).date()
        # self.bank_manager.start_day_recalculation()
        for transaction in self.bank_manager.executed_transaction_history[::-1]:
            if transaction.execution_time.date() >= new_time_date:
                self.bank_manager.cancel_transaction(transaction)
                self.bank_manager.executed_transaction_history.pop(-1)
            else:
                break
        self.time_controller.set_time(prev_time - timedelta(days=1))

    def skip_to_date(self, to_date: date):
        if to_date == self.time_controller.get_curr_time().date():
            return
        if to_date > self.time_controller.get_curr_time().date():
            while to_date > self.time_controller.get_curr_time().date():
                self.next_day()
        if to_date < self.time_controller.get_curr_time().date():
            while to_date < self.time_controller.get_curr_time().date():
                self.prev_day()
