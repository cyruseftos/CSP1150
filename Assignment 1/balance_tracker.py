# Author: Cyrus Eftos <cyruse@our.ecu.edu.au>
# Student ID: 10434000
#
# Assignment 1: Individual Programming Assignment
#
# Implements a “Balance Tracker” program in which the user enters an initial balance value and can then add or subtract
# amounts from this value. The program keeps track of these transactions, and allow the user to see the current
# balance as well as information about the transactions that have been made.

def num_to_currency(number):
    return "${:0,.2f}".format(number).replace("$-", "-$")  # http://stackoverflow.com/a/42753618


def show_info(value_list, type_list, desired_type):
    count = 0
    total = 0

    for i, item in enumerate(type_list):
        if item == desired_type:
            count += 1
            total += value_list[i]

    if count != 0:
        print("---", desired_type, "---")
        print(desired_type, "count:", count)
        print(desired_type, "total:", num_to_currency(total))
        print("\n")
    else:
        print("No", desired_type, "transaction records entered.")


def plural(value_list):
    return "transaction" if len(value_list) == 1 else "transactions"  # if value is 1 return singular else return plural


def test_input(prompt, error_message="\nPlease enter a valid number! \n"):
    while True:
        user_input = input(prompt)
        try:
            num_response = float(user_input)
        except ValueError:
            print(error_message)
            continue
        if num_response <= 0:  # Should you be able to start with a balance of 0?
            print("Please enter a number greater than 0.00 ")
            continue

        return num_response


def main():  # Program
    menu_options = ("[A]ddition", "[S]ubtraction", "[H]istory", "[I]nformation", "[Q]uit")  # menu options
    transaction_amounts = []  # Declare empty "transaction_amounts" list
    transaction_types = []  # Declare empty "transaction_types" list

    print("Welcome to Balance Tracker!\n")

    balance = test_input("Enter starting balance: ")  # Prompt the user to enter the initial value
    transaction_amounts.append(balance)  # Append initial balance to transactions_amounts list
    transaction_types.append("Starting Balance")  # Append "Starting Balance"

    while True:
        print("Current balance is:", num_to_currency(balance))
        print("Choose from the following options:\n")

        for option in menu_options:
            print(option)  # Loop through the menu tuple and print out the values.

        user_input = input("\n> ").upper()

        if user_input == "A":
            amount = test_input("Add to balance: ")
            transaction_amounts.append(amount)  # Append amount to transaction_amounts list
            transaction_types.append("Addition")  # Append "Addition" to transaction_types list
            balance += amount  # Add amount to the balance

        elif user_input == "S":
            if balance <= 0:
                print("WARNING! Your balance is currently negative, please [A]dd to your balance to continue.\n")
                continue

            amount = test_input("Subtract from balance: ")
            transaction_amounts.append(amount)  # Append amount to transaction_amounts list
            transaction_types.append("Subtraction")  # Append "Subtraction" to transaction_types list
            balance -= amount  # Subtract amount from balance
            print("\n!!! Warning: Your balance is now negative !!!\n" if balance < -1 else "")  # Neg Balance Warn

        elif user_input == "H":
            print("--- Transaction History ---\n")
            print("Starting balance was", num_to_currency(transaction_amounts[0]))
            # Loop through transactionAmount but cut off the first value as this is where we store the initial balance.
            for i, amount in enumerate(transaction_amounts[1:]):
                print("Transaction", i + 1, "-", transaction_types[i + 1], "of", num_to_currency(amount))
            print("\n--- Total of", len(transaction_amounts[1:]), plural(transaction_amounts[1:]), "---\n")

        elif user_input == "I":
            show_info(transaction_amounts, transaction_types, "Addition")
            show_info(transaction_amounts, transaction_types, "Subtraction")

        elif user_input == "Q":
            break

        else:
            print("Please enter a valid option!\n")

    print("Goodbye!")


main()
