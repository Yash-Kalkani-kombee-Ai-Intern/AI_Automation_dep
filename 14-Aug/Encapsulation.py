class BankAccount:

    def __init__(self, name, balance):
        self.name = name
        self.__balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print("Amount deposited successfully.")
        else:
            print("Invalid amount.")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.__balance:
            self.__balance -= amount
            print("Amount withdrawn successfully.")
        else:
            print("Insufficient balance or invalid amount.")

    def show_account(self):
        print("\n--- Account Details ---")
        print("Name:", self.name)
        print("Balance:", self.__balance)


# User Input
name = input("Enter your name: ")
initial_balance = float(input("Enter initial balance: "))

account = BankAccount(name, initial_balance)

while True:

    print("\n1. Deposit")
    print("2. Withdraw")
    print("3. Show Account")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        amount = float(input("Enter deposit amount: "))
        account.deposit(amount)

    elif choice == "2":
        amount = float(input("Enter withdrawal amount: "))
        account.withdraw(amount)

    elif choice == "3":
        account.show_account()

    elif choice == "4":
        print("Thank you!")
        break

    else:
        print("Invalid choice.")

        
#output====================================
""" Enter your name: Yash
Enter initial balance: 2000

1. Deposit
2. Withdraw
3. Show Account
4. Exit
Enter your choice: 1
Enter deposit amount: 20000
Amount deposited successfully.

1. Deposit
2. Withdraw
3. Show Account
4. Exit
Enter your choice: 2
Enter withdrawal amount: 3000
Amount withdrawn successfully.

1. Deposit
2. Withdraw
3. Show Account
4. Exit
Enter your choice: 3

--- Account Details ---
Name: Yash
Balance: 19000.0

1. Deposit
2. Withdraw
3. Show Account
4. Exit
Enter your choice: 4
Thank you!"""