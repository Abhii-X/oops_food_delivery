from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.base import Base
from database.connection import engine

from database.customer_model import CustomerModel
from database.restaurant_model import RestaurantModel
from database.food_model import FoodModel
from database.order_model import OrderModel
from database.order_item_model import OrderItemModel
from database.payment_model import PaymentModel
from database.delivery_model import DeliveryModel

from routes.customer_routes import router as customer_router
from routes.restaurant_routes import router as restaurant_router
from routes.food_routes import router as food_router
from routes.order_routes import router as order_router
from routes.payment_routes import router as payment_router
from routes.delivery_routes import router as delivery_router


Base.metadata.create_all(bind=engine)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(customer_router)
app.include_router(restaurant_router)
app.include_router(food_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(delivery_router)


@app.get("/")
def home():
    return {
        "message": "Food Delivery API is running"
    }