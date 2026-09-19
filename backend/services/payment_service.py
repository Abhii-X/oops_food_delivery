from models.payment import Payment

from database.order_model import OrderModel
from database.order_item_model import OrderItemModel
from database.food_model import FoodModel
from database.payment_model import PaymentModel


class PaymentService:

    def process_payment(self, db, order_id, method):

        order_model = db.query(OrderModel).filter(
            OrderModel.id == order_id
        ).first()

        if not order_model:
            return None

        order_items = db.query(OrderItemModel).filter(
            OrderItemModel.order_id == order_id
        ).all()

        total = 0

        for item in order_items:

            food = db.query(FoodModel).filter(
                FoodModel.id == item.food_id
            ).first()

            total += food.price * item.quantity

        payment = Payment(
            0,
            order_model,
            total,
            method
        )

        payment.process_payment()

        payment_model = PaymentModel(
            order_id=order_id,
            amount=payment.amount,
            method=payment.method,
            status=payment.status
        )

        db.add(payment_model)
        db.commit()
        db.refresh(payment_model)

        return payment_model

    def get_payments(self, db):
        return db.query(PaymentModel).all()

    def get_payment(self, db, payment_id):

        return db.query(PaymentModel).filter(
            PaymentModel.id == payment_id
        ).first()

    def update_payment_status(
        self,
        db,
        payment_id,
        status
    ):

        payment_model = db.query(PaymentModel).filter(
            PaymentModel.id == payment_id
        ).first()

        if not payment_model:
            return None

        payment = Payment(
            payment_model.id,
            payment_model.order_id,
            payment_model.amount,
            payment_model.method
        )

        payment.status = payment_model.status

        if status == "REFUNDED":
            payment.refund_payment()
        else:
            payment.status = status

        payment_model.status = payment.status

        db.commit()
        db.refresh(payment_model)

        return payment_model