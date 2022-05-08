import enum


class Transaction:
    def __init__(self, amount: int, bank_from_id: int, bank_to_id: int, account_from_id: int, account_to_id: int,
                 forced: bool = False):
        self.id = None
        self.amount = amount
        self.bank_from_id = bank_from_id
        self.bank_to_id = bank_to_id
        self.account_from_id = account_from_id
        self.account_to_id = account_to_id
        self.forced = forced
        self.state = TransactionState.UNEXECUTED


class TransactionState(enum):
    UNEXECUTED = 0
    EXECUTED = 1
    CANCELLED = 2
