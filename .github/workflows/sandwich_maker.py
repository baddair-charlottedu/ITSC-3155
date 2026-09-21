class SandwichMachine:

    def __init__(self, machine_resources):
        """Receives resources as input."""
        self.machine_resources = machine_resources

    def check_resources(self, ingredients):
        """Returns True when order can be made, False if ingredients are insufficient."""
        for item, amount_needed in ingredients.items():
            if self.machine_resources[item] < amount_needed:
                print(f"Sorry there is not enough {item}.")
                return False

        return True

    def make_sandwich(self, sandwich_size, order_ingredients):
        """Deduct the required ingredients from the resources."""
        for item, amount_needed in order_ingredients.items():
            self.machine_resources[item] -= amount_needed

        print(f"{sandwich_size} sandwich is ready. Bon appetit!")