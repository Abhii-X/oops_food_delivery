class Order:
    def __init__(self, order_id, customer, items):
        self.order_id = order_id
        self.customer = customer
        self.items = items
        self.status = "PLACED"

    def calculate_total(self):
        total = 0

        for item in self.items:
            total += item.get_total()

        return total

    def update_status(self, status):
        self.status = status

    def cancel_order(self):
        self.status = "CANCELLED"