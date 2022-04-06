class Address:
    def __init__(self):
        self.street = None
        self.city = None
        self.region = None
        self.postal_code = None
        self.country = None

    def validate(self) -> bool:
        pass


class ATM:
    def __init__(self):
        self.bank = None
        self.current_user = None

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
