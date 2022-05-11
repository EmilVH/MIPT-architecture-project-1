from typing import Optional

import banks.entities
import banks.managers

class ATM:
    def __init__(self, bank_manager: banks.managers.BankManager, bank: banks.entities.Bank):
        self.bank_manager = bank_manager
        self.bank = bank
        self.current_user: Optional[banks.entities.Client] = None

    @staticmethod
    def _check_active_user(func):
        def wrapper(self):
            if self.current_user is None:
                return False
                # or maybe I should throw exception here
            else:
                func(self)

        return wrapper

    @_check_active_user
    def add_cash(self):
        pass

    def get_cash(self):
        pass

    def register_client(self):
        pass

    def login(self):
        pass

    def add_address(self):
        pass

    def add_id_number(self):
        pass

    def show_account(self):
        pass

    def end_session(self):
        pass

