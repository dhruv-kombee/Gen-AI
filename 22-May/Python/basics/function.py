accounts = {}

def create_account():
    name = input("Enter your name: ")
    if name in accounts:
        print("Account already exists.")
    else:
        accounts[name] = 0
        print("Account created successfully.")

def deposit(name):
    amount = int(input("Enter amount to deposit: "))
    if amount > 0:
        accounts[name] += amount
        print("Amount deposited successfully.")
        print("Current Balance:", accounts[name])
    else:
        print("Invalid amount.")

def withdraw(name):
    amount = int(input("Enter amount to withdraw: "))
    if amount <= 0:
        print("Invalid amount.")
    elif amount > accounts[name]:
        print("Insufficient balance.")
    else:
        accounts[name] -= amount
        print("Withdrawal successful.")
        print("Current Balance:", accounts[name])

def show_account(name):
    print("Name :", name)
    print("Balance :", accounts[name])

def access_account():
    name = input("Enter member name: ")
    if name in accounts:
        while True:
            show_account(name)
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Exit")
            choice = input("Enter option: ")
            if choice == "1":
                deposit(name)
            elif choice == "2":
                withdraw(name)
            elif choice == "3":
                break
            else:
                print("Invalid option.")
    else:
        print("Account not found.")

def show_members():
    if len(accounts) == 0:
        print("No accounts found.")
        return
    for name in accounts:
        print(name)
    search_name = input("Enter member name: ")
    if search_name in accounts:
        show_account(search_name)
    else:
        print("Account not found.")

while True:
    print("\n1. Create Account")
    print("2. Access Account")
    print("3. Show Member Details")
    print("0. Exit")
    option = input("Enter option: ")
    if option == "1":
        create_account()
    elif option == "2":
        access_account()
    elif option == "3":
        show_members()
    elif option == "0":
        print("Program exited.")
        break
    else:
        print("Invalid option.")