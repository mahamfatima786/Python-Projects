# Simple Coffee Shop App - 2 Min Project

menu = {
    "Espresso": 350,
    "Latte": 450,
    "Cappuccino": 500,
    "Americano": 400,
    "Mocha": 550
}

cart = []
total = 0

def show_menu():
    print("\n--- Our COFFEE MENU ---")
    for i, (coffee, price) in enumerate(menu.items(), 1):
        print(f"{i}. {coffee} - Rs. {price}")

def take_order():
    global total
    while True:
        show_menu()
        choice = input("\nEnter number (1-5) to add, or 'done' to checkout: ").lower()

        if choice == 'done':
            break

        if choice.isdigit() and 1 <= int(choice) <= len(menu):
            coffee_name = list(menu.keys())[int(choice)-1]
            cart.append(coffee_name)
            total += menu[coffee_name]
            print(f"Added {coffee_name}! Current total: Rs. {total}")
        else:
            print("Invalid choice, try again!")

def checkout():
    if not cart:
        print("\nYou didn't order anything!")
        return
    print("\n--- YOUR BILL ---")
    for item in cart:
        print(f"- {item}: Rs. {menu[item]}")
    print(f"TOTAL: Rs. {total}")
    print("Thanks for visiting Our Coffee Shop! ☕")

# Run the app
print("Welcome to Our Coffee Shop!")
take_order()
checkout()