### Data ###

recipes = {
    "small": {
        "ingredients": {
            "bread": 2,  ## slice
            "ham": 4,  ## slice
            "cheese": 4,  ## ounces
        },
        "cost": 1.75,
    },
    "medium": {
        "ingredients": {
            "bread": 4,  ## slice
            "ham": 6,  ## slice
            "cheese": 8,  ## ounces
        },
        "cost": 3.25,
    },
    "large": {
        "ingredients": {
            "bread": 6,  ## slice
            "ham": 8,  ## slice
            "cheese": 12,  ## ounces
        },
        "cost": 5.5,
    }
}

resources = {
    "bread": 12,  ## slice
    "ham": 18,  ## slice
    "cheese": 24,  ## ounces
}


### Complete functions ###

class SandwichMachine:

    def __init__(self, machine_resources):
        """Receives resources as input.
           Hint: bind input variable to self variable"""
        self.machine_resources = machine_resources

    def check_resources(self, ingredients):
        """Returns True when order can be made, False if ingredients are insufficient."""
        for item, amount_needed in ingredients.items():
            if self.machine_resources[item] < amount_needed:
                print(f"Sorry there is not enough {item}.")
                return False
        return True

    def process_coins(self):
        """Returns the total calculated from coins inserted.
           Hint: include input() function here, e.g. input("how many quarters?: ")"""
        print("Please insert coins.")
        large_dollars = int(input("how many large dollars?: "))
        half_dollars = int(input("how many half dollars?: "))
        quarters = int(input("how many quarters?: "))
        nickels = int(input("how many nickels?: "))

        total = (large_dollars * 1) + (half_dollars * 0.5) + (quarters * 0.25) + (nickels * 0.05)
        return total

    def transaction_result(self, coins, cost):
        """Return True when the payment is accepted, or False if money is insufficient.
           Hint: use the output of process_coins() function for cost input"""
        if coins < cost:
            print("Sorry that's not enough money. Money refunded.")
            return False

        change = round(coins - cost, 2)
        print(f"Here is ${change} in change.")
        return True

    def make_sandwich(self, sandwich_size, order_ingredients):
        """Deduct the required ingredients from the resources.
           Hint: no output"""
        for item, amount_needed in order_ingredients.items():
            self.machine_resources[item] -= amount_needed
        print(f"{sandwich_size} sandwich is ready. Bon appetit!")


### Make an instance of SandwichMachine class and write the rest of the codes ###

def show_report(machine_resources):
    print(f"Bread: {machine_resources['bread']} slice(s)")
    print(f"Ham: {machine_resources['ham']} slice(s)")
    print(f"Cheese: {machine_resources['cheese']} pound(s)")


def main():
    machine = SandwichMachine(resources)
    is_on = True

    while is_on:
        choice = input("What would you like? (small/ medium/ large/ off/ report): ").strip().lower()

        if choice == "off":
            is_on = False

        elif choice == "report":
            show_report(machine.machine_resources)

        elif choice in recipes:
            order = recipes[choice]
            ingredients = order["ingredients"]
            cost = order["cost"]

            if machine.check_resources(ingredients):
                coins = machine.process_coins()

                if machine.transaction_result(coins, cost):
                    machine.make_sandwich(choice, ingredients)

        else:
            print("Please choose a valid option.")


if __name__ == "__main__":
    main()
