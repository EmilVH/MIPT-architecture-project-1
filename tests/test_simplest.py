import unittest
from datetime import timedelta

import banks.accounts
import banks.utils
from banks.core import Transaction
from banks.entities import Client, Bank
from banks.managers import BankManager, RecalculationManager
from banks.time_controller import get_time


class SimpleSetup(unittest.TestCase):
    bank_manager = None
    recalculation_manager = None
    bank_1: Bank = None
    bank_2: Bank = None
    client_1: Client = None
    client_2: Client = None
    debit_account_1: banks.accounts.Account = None
    credit_account_1: banks.accounts.Account = None
    debit_account_2: banks.accounts.Account = None

    @classmethod
    def setUpClass(cls):
        cls.bank_manager = BankManager()
        cls.recalculation_manager = RecalculationManager(cls.bank_manager)
        cls.bank_1 = cls.bank_manager.create_bank("BANK 1")
        cls.bank_2 = cls.bank_manager.create_bank("BANK 2")
        cls.client_1 = Client('Ivan', 'Ivanonv',
                              banks.utils.Address('Pervomayskaya 32', 'Dolgoprudniy', 'Moscow oblast', 123123,
                                                  'Russia'), 12381938)
        cls.bank_1.add_client(cls.client_1)
        cls.client_2 = Client('Peter', 'Petrov',
                              banks.utils.Address('Centralnaya 54', 'Moscow', 'Moscow', 4201230, 'Russia'), 4838726723)
        cls.bank_2.add_client(cls.client_2)
        cls.debit_account_1 = cls.bank_1.add_account(cls.client_1, banks.accounts.AccountType.Debit)
        cls.debit_account_1.balance = 10000
        cls.credit_account_1 = cls.bank_1.add_account(cls.client_1, banks.accounts.AccountType.Credit)
        cls.credit_account_1.balance = -500
        cls.deposit_account_1 = cls.bank_1.add_account(cls.client_1, banks.accounts.AccountType.Deposit)
        cls.bank_1.deposit_open(cls.deposit_account_1, cls.bank_1.bank_account, 600000)
        cls.debit_account_2 = cls.bank_2.add_account(cls.client_2, banks.accounts.AccountType.Debit)
        cls.debit_account_2.balance = 10000
        print('Set up')


class TestCreation(SimpleSetup):

    def test_balance_initial(self):
        self.assertEqual(self.debit_account_1.balance, 10000)
        self.assertEqual(self.debit_account_2.balance, 10000)
        self.assertTrue(self.debit_account_1.account_id in self.bank_1.all_accounts)

    def test_exists(self):
        self.assertTrue(self.debit_account_1.account_id in self.bank_1.all_accounts)
        self.assertTrue(self.debit_account_2.account_id in self.bank_2.all_accounts)
        self.assertTrue(str(self.client_1) in self.bank_1.all_clients)
        self.assertTrue(str(self.client_2) in self.bank_2.all_clients)
        self.assertTrue(self.bank_1.bank_id in self.bank_manager.all_banks)
        self.assertTrue(self.bank_2.bank_id in self.bank_manager.all_banks)


class TestSend(SimpleSetup):
    def test_send(self):
        transaction = Transaction(1000, self.bank_1.bank_id, self.bank_2.bank_id, self.debit_account_1.account_id,
                                  self.debit_account_2.account_id)
        self.assertTrue(self.bank_manager.execute_transaction(transaction))
        self.assertEqual(9000, self.debit_account_1.balance)
        self.assertEqual(11000, self.debit_account_2.balance)


class TestSendCancel(SimpleSetup):
    def test_send_cancel(self):
        transaction = Transaction(1000, self.bank_1.bank_id, self.bank_2.bank_id, self.debit_account_1.account_id,
                                  self.debit_account_2.account_id)
        self.assertTrue(self.bank_manager.execute_transaction(transaction))
        self.assertEqual(9000, self.debit_account_1.balance)
        self.assertEqual(11000, self.debit_account_2.balance)
        self.bank_manager.cancel_transaction(transaction)
        self.assertEqual(10000, self.debit_account_1.balance)
        self.assertEqual(10000, self.debit_account_2.balance)


class TestRecalculation1day(SimpleSetup):
    def test_1_day_recalc(self):
        self.recalculation_manager.next_day()
        self.assertEqual(self.debit_account_1.balance, 10002)
        self.assertEqual(-600, self.credit_account_1.balance)
        self.assertEqual(600328, self.deposit_account_1.balance)


class TestLongRecalculation(SimpleSetup):
    def test_1_year_recalc(self):
        self.recalculation_manager.skip_to_date((get_time() + timedelta(days=365)).date())
        self.assertEqual(self.debit_account_1.balance, 10730)
        self.assertEqual(self.credit_account_1.balance, -37000)
        self.assertEqual(self.deposit_account_1.balance, 732598)


class TestTimeSkipping1(SimpleSetup):
    def test_1_year_forward_and_back(self):
        self.recalculation_manager.skip_to_date((get_time() + timedelta(days=365)).date())
        self.assertEqual(self.debit_account_1.balance, 10730)
        self.assertEqual(self.credit_account_1.balance, -37000)
        self.assertEqual(self.deposit_account_1.balance, 732598)
        self.recalculation_manager.skip_to_date((get_time() - timedelta(days=365)).date())
        self.assertEqual(self.debit_account_1.balance, 10000)
        self.assertEqual(self.deposit_account_1.balance, 600000)
        self.assertEqual(self.credit_account_1.balance, -500)
class TestTimeSkipping2(SimpleSetup):
    def test_1_day_forward_and_back(self):
        self.recalculation_manager.skip_to_date((get_time() + timedelta(days=1)).date())
        self.assertEqual(self.debit_account_1.balance, 10002)
        self.assertEqual(-600, self.credit_account_1.balance)
        self.assertEqual(600328, self.deposit_account_1.balance)
        self.recalculation_manager.skip_to_date((get_time() - timedelta(days=1)).date())
        self.assertEqual(self.debit_account_1.balance, 10000)
        self.assertEqual(self.deposit_account_1.balance, 600000)
        self.assertEqual(self.credit_account_1.balance, -500)

if __name__ == '__main__':
    unittest.main()
