from models.customer import Customer
from models.food import Food
from models.restaurant import Restaurant
from models.order_item import OrderItem
from models.cart import Cart
from models.order import Order
from models.payment import Payment
from models.delivery import Delivery


customer = Customer(
    "Abhii",
    "abhii@gmail.com",
    "9876543210",
    "Salem"
)

restaurant = Restaurant(
    1,
    "Food Palace",
    "Salem"
)

food1 = Food(
    1,
    "Chicken Biryani",
    180,
    "Main Course"
)

food2 = Food(
    2,
    "Burger",
    120,
    "Fast Food"
)

restaurant.add_food(food1)
restaurant.add_food(food2)

item1 = OrderItem(food1, 2)
item2 = OrderItem(food2, 1)

cart = Cart(customer)

cart.add_item(item1)
cart.add_item(item2)

print("Cart total:", cart.calculate_total())

order = Order(
    1,
    customer,
    cart.items
)

print("Order total:", order.calculate_total())
print("Order status:", order.status)

payment = Payment(
    1,
    order,
    order.calculate_total(),
    "UPI"
)

payment.process_payment()

print("Payment status:", payment.status)

delivery = Delivery(
    1,
    order,
    customer.address
)

delivery.assign_delivery()

print("Delivery status:", delivery.status)