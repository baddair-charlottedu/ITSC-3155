import data
import cashier
import sandwich_maker


recipes = data.recipes
resources = data.resources


def show_report(machine_resources):
    print(f"Bread: {machine_resources['bread']} slice(s)")
    print(f"Ham: {machine_resources['ham']} slice(s)")
    print(f"Cheese: {machine_resources['cheese']} ounce(s)")


def main():
    machine = sandwich_maker.SandwichMachine(resources)
    cashier_machine = cashier.Cashier()

    is_on = True

    while is_on:
        choice = input(
            "What would you like? (small/ medium/ large/ off/ report): "
        ).strip().lower()

        if choice == "off":
            is_on = False

        elif choice == "report":
            show_report(machine.machine_resources)

        elif choice in recipes:
            order = recipes[choice]
            ingredients = order["ingredients"]
            cost = order["cost"]

            if machine.check_resources(ingredients):
                coins = cashier_machine.process_coins()

                if cashier_machine.transaction_result(coins, cost):
                    machine.make_sandwich(choice, ingredients)

        else:
            print("Please choose a valid option.")


if __name__ == "__main__":
    main()