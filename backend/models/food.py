class Food:
    def __init__(self, food_id, name, price, category):
        self.food_id = food_id
        self.name = name
        self.price = price
        self.category = category

    def update_price(self, price):
        self.price = price