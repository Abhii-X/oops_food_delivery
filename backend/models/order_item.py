class OrderItem:
    def __init__(self, food, quantity):
        self.food = food
        self.quantity = quantity

    def get_total(self):
        return self.food.price * self.quantity