from models.customer import Customer
from models.food import Food
from models.order import Order
from models.order_item import OrderItem

from database.customer_model import CustomerModel
from database.food_model import FoodModel
from database.order_model import OrderModel
from database.order_item_model import OrderItemModel


class OrderService:

    def create_order(self, db, customer_id, items):

        customer_model = db.query(CustomerModel).filter(
            CustomerModel.id == customer_id
        ).first()

        if not customer_model:
            return None

        customer = Customer(
            customer_model.name,
            customer_model.email,
            customer_model.phone,
            customer_model.address
        )

        order_items = []

        for item in items:

            food_model = db.query(FoodModel).filter(
                FoodModel.id == item.food_id
            ).first()

            if not food_model:
                return None

            food = Food(
                food_model.id,
                food_model.name,
                food_model.price,
                food_model.category
            )

            order_item = OrderItem(
                food,
                item.quantity
            )

            order_items.append(order_item)

        order = Order(
            0,
            customer,
            order_items
        )

        order_model = OrderModel(
            customer_id=customer_id,
            status=order.status
        )

        db.add(order_model)
        db.flush()

        for item in order_items:

            order_item_model = OrderItemModel(
                order_id=order_model.id,
                food_id=item.food.food_id,
                quantity=item.quantity
            )

            db.add(order_item_model)

        db.commit()
        db.refresh(order_model)

        return order_model, order

    def get_orders(self, db):
        return db.query(OrderModel).all()

    def get_order(self, db, order_id):

        order_model = db.query(OrderModel).filter(
            OrderModel.id == order_id
        ).first()

        if not order_model:
            return None

        customer_model = db.query(CustomerModel).filter(
            CustomerModel.id == order_model.customer_id
        ).first()

        order_item_models = db.query(OrderItemModel).filter(
            OrderItemModel.order_id == order_id
        ).all()

        customer = Customer(
            customer_model.name,
            customer_model.email,
            customer_model.phone,
            customer_model.address
        )

        order_items = []

        for item in order_item_models:

            food_model = db.query(FoodModel).filter(
                FoodModel.id == item.food_id
            ).first()

            food = Food(
                food_model.id,
                food_model.name,
                food_model.price,
                food_model.category
            )

            order_item = OrderItem(
                food,
                item.quantity
            )

            order_items.append(order_item)

        order = Order(
            order_model.id,
            customer,
            order_items
        )

        order.status = order_model.status

        return order

    def update_order_status(
        self,
        db,
        order_id,
        status
    ):

        order_model = db.query(OrderModel).filter(
            OrderModel.id == order_id
        ).first()

        if not order_model:
            return None

        order = self.get_order(
            db,
            order_id
        )

        if not order:
            return None

        order.update_status(status)

        order_model.status = order.status

        db.commit()
        db.refresh(order_model)

        return order_model

    def cancel_order(self, db, order_id):

        order_model = db.query(OrderModel).filter(
            OrderModel.id == order_id
        ).first()

        if not order_model:
            return None

        order = self.get_order(
            db,
            order_id
        )

        if not order:
            return None

        order.cancel_order()

        order_model.status = order.status

        db.commit()
        db.refresh(order_model)

        return order_model