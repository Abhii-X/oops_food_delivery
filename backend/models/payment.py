class Payment:
    def __init__(self, payment_id, order, amount, method):
        self.payment_id = payment_id
        self.order = order
        self.amount = amount
        self.method = method
        self.status = "PENDING"

    def process_payment(self):
        self.status = "SUCCESS"

    def refund_payment(self):
        self.status = "REFUNDED"