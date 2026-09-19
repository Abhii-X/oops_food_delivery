class Delivery:
    def __init__(self, delivery_id, order, address):
        self.delivery_id = delivery_id
        self.order = order
        self.address = address
        self.status = "PENDING"

    def assign_delivery(self):
        self.status = "ASSIGNED"

    def update_status(self, status):
        self.status = status