from models.delivery import Delivery

from database.order_model import OrderModel
from database.customer_model import CustomerModel
from database.delivery_model import DeliveryModel


class DeliveryService:

    def create_delivery(self, db, order_id):

        order_model = db.query(OrderModel).filter(
            OrderModel.id == order_id
        ).first()

        if not order_model:
            return None

        customer_model = db.query(CustomerModel).filter(
            CustomerModel.id == order_model.customer_id
        ).first()

        if not customer_model:
            return None

        delivery = Delivery(
            0,
            order_model,
            customer_model.address
        )

        delivery.assign_delivery()

        delivery_model = DeliveryModel(
            order_id=order_id,
            address=delivery.address,
            status=delivery.status
        )

        db.add(delivery_model)
        db.commit()
        db.refresh(delivery_model)

        return delivery_model

    def get_deliveries(self, db):
        return db.query(DeliveryModel).all()

    def get_delivery(self, db, delivery_id):

        return db.query(DeliveryModel).filter(
            DeliveryModel.id == delivery_id
        ).first()

    def update_delivery_status(
        self,
        db,
        delivery_id,
        status
    ):

        delivery_model = db.query(DeliveryModel).filter(
            DeliveryModel.id == delivery_id
        ).first()

        if not delivery_model:
            return None

        delivery = Delivery(
            delivery_model.id,
            delivery_model.order_id,
            delivery_model.address
        )

        delivery.status = delivery_model.status

        delivery.update_status(status)

        delivery_model.status = delivery.status

        db.commit()
        db.refresh(delivery_model)

        return delivery_model