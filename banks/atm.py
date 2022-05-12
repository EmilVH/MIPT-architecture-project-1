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

    def _get_user_selection(self, selection: dict):
        order = dict()
        num = 0
        promt = "Enter your choise:\n"
        for key, name in selection:
            num += 1
            order[num] = key
            promt += "{}) name\n".format(num)
        entered = False
        while not entered:
            try:
                res = input(promt)
                res_val = int(res)
                if res_val in order:
                    print('Error, enter again')
                    entered = True
            except:
                print('Error, enter again')
        return selection[order[res_val]]

