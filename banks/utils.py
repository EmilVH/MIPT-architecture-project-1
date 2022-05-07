class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


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


class UniqueIdGeneratorSingleton(metaclass=Singleton):
    def __init__(self):
        self.curr_id = 0

    def generate_new_unique_id(self) -> int:
        self.curr_id += 1
        return self.curr_id


def get_unique_id() -> int:
    return UniqueIdGeneratorSingleton().generate_new_unique_id()
