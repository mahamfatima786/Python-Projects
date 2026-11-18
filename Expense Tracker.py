# Expense Tracker (No Functions):)
expenses = [] # List of expense dictionaries.
print("😊Welcome to Expense Tracker💰")
while True :
    print("\n==========MENU==========")
    print("1. Add Expense.")
    print("2. View All Expense.")
    print("3. View Total Spending.")
    print("4. View Spending by Category.")
    print("5. Exit.")
    print("======================")
    choice = input("Enter your choice(1-5):")

# Add Expense

    if choice == "1" :
        date = input("Enter Date (DD-MM-YYYY):")
        category = input("Enter Category(Food,Travel,Shopping,etc.)")
        description = input("Enter Short Description:")
        amount = float(input("Enter Amount:"))

        expense = {
            "date" : date,
            "category" : category,
            "description" : description,
            "amount" : amount,
        }
        expenses.append(expense)
        print("\nExpense Added Successfully!😉")

# View All Expenses
    elif choice == "2":
        if len(expenses) == 0:
            print(" \nNo Expenses Recorded Yet.☹️")
        else:
            print("\n-----------------All Expenses-----------------")
            i = 1
            for e in expenses :
                print(f"{i} . {e['date']} {e['category']} {e['description']} {e['amount']} ")
                i += 1
                print("--------------------------------------------")
    # Total & Category Summary
    elif choice == "3":
        total = 0
        for e in expenses :
            total = e['amount']
        print(f"\nTotal Spending = {total}")
    elif choice == "4":
        if len(expenses) == 0:
                    print("\n No Expenses Recorded Yet.☹️")
        else:
            summary = {}
            for e in expenses:
                cat = e["category"]
                if cat in summary:
                    summary[cat] += e["amount"]
                else:
                    summary[cat] = e["amount"]
            print("\n Spending by Category:")
            for cat, amt in summary.items():
                print(f"{cat}: n{amt}")
# Exit              
    elif choice == "5":
        print("\n Thanks for using Expense Tracker! Bye!👋🏻")
        break    
    else:
        print("\n  Invalid choice. Please try again.☹️")