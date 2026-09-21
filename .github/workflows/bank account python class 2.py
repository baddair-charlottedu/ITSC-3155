# bank_account_python 2.py
# BankAccount, SavingsAccount, CheckingAccount, and main program
# authors: Brandon Addair


# BASE CLASS: BankAccount
class BankAccount:
    def __init__(self, customer_name, current_balance, minimum_balance, bank_title,
                 account_number, routing_number):
        self.customer_name = customer_name
        self.current_balance = current_balance
        self.minimum_balance = minimum_balance
        self.bank_title = bank_title

        # protected member (single underscore) - accessible to subclasses
        self._account_number = account_number

        # private member (double underscore) - name-mangled, not directly accessible outside class
        self.__routing_number = routing_number

    def deposit(self, amount):
        self.current_balance += amount

    def withdraw(self, amount):
        if amount > self.current_balance - self.minimum_balance:
            print("Withdraw amount invalid! Not enough funds")
        else:
            self.current_balance -= amount

    def get_routing_number(self):
        # controlled access to the private member
        return self.__routing_number

    def print_customer_information(self):
        print("Customer name: " + self.customer_name)
        print("Current balance: " + str(self.current_balance))
        print("Minimum balance: " + str(self.minimum_balance))
        print("Bank title: " + self.bank_title)
        print("Account number: " + str(self._account_number))



# SUBCLASS: SavingsAccount (adds interest)
class SavingsAccount(BankAccount):
    def __init__(self, customer_name, current_balance, minimum_balance, bank_title,
                 account_number, routing_number, interest_rate):
        super().__init__(customer_name, current_balance, minimum_balance, bank_title,
                          account_number, routing_number)
        self.interest_rate = interest_rate  # e.g. 0.02 for 2%

    def apply_interest(self):
        interest_earned = self.current_balance * self.interest_rate
        self.current_balance += interest_earned
        print(f"Interest applied: ${interest_earned:.2f} | New balance: ${self.current_balance:.2f}")



# SUBCLASS: CheckingAccount (adds transfer limitation)
class CheckingAccount(BankAccount):
    def __init__(self, customer_name, current_balance, minimum_balance, bank_title,
                 account_number, routing_number, transfer_limit):
        super().__init__(customer_name, current_balance, minimum_balance, bank_title,
                          account_number, routing_number)
        self.transfer_limit = transfer_limit
        self.transfers_made = 0

    def transfer(self, amount, recipient_name):
        if self.transfers_made >= self.transfer_limit:
            print("Transfer denied! Monthly transfer limit reached.")
        elif amount > self.current_balance - self.minimum_balance:
            print("Transfer denied! Not enough funds.")
        else:
            self.current_balance -= amount
            self.transfers_made += 1
            print(f"Transferred ${amount:.2f} to {recipient_name}. "
                  f"Transfers used: {self.transfers_made}/{self.transfer_limit}")


# MAIN PROGRAM
def main():
    # --- Two SavingsAccount instances (required: 2 instances) ---
    savings1 = SavingsAccount("Alice Johnson", 1000, 100, "First National Bank",
                               "SA-1001", "RT-2001", 0.03)
    savings2 = SavingsAccount("Ben Carter", 5000, 500, "First National Bank",
                               "SA-1002", "RT-2002", 0.015)

    # --- Two CheckingAccount instances (required: 2 instances) ---
    checking1 = CheckingAccount("Carla Diaz", 800, 50, "First National Bank",
                                 "CH-3001", "RT-4001", 3)
    checking2 = CheckingAccount("David Kim", 2000, 100, "First National Bank",
                                 "CH-3002", "RT-4002", 5)

    # --- The one required scenario: Carla opens a checking account and withdraws $200 ---
    print("=== Scenario: Carla opens a checking account and withdraws $200 ===")
    checking1.print_customer_information()
    checking1.withdraw(200)
    print("Balance after withdrawal:", checking1.current_balance)


if __name__ == "__main__":
    main()