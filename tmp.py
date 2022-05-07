from banks.accounts import DepositAccount

ac = DepositAccount(1, 2, 3, 5.0)
ac.add_money(500)
print(ac.balance)
print(ac.recalculate_day())
