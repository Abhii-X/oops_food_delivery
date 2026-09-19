class Restaurant:
    def __init__(self, restaurant_id, name, address):
        self.restaurant_id = restaurant_id
        self.name = name
        self.address = address
        self.menu = []

    def add_food(self, food):
        self.menu.append(food)

    def remove_food(self, food):
        if food in self.menu:
            self.menu.remove(food)

    def view_menu(self):
        return self.menu