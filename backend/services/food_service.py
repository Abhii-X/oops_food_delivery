from models.food import Food

from database.food_model import FoodModel
from database.restaurant_model import RestaurantModel


class FoodService:

    def create_food(
        self,
        db,
        name,
        price,
        category,
        restaurant_id
    ):
        restaurant = db.query(RestaurantModel).filter(
            RestaurantModel.id == restaurant_id
        ).first()

        if not restaurant:
            return None

        food = Food(
            0,
            name,
            price,
            category
        )

        food_model = FoodModel(
            name=food.name,
            price=food.price,
            category=food.category,
            restaurant_id=restaurant_id
        )

        db.add(food_model)
        db.commit()
        db.refresh(food_model)

        return food_model

    def get_foods(self, db):
        return db.query(FoodModel).all()

    def get_food(self, db, food_id):
        return db.query(FoodModel).filter(
            FoodModel.id == food_id
        ).first()

    def update_food(
        self,
        db,
        food_id,
        name,
        price,
        category,
        restaurant_id
    ):
        food_model = db.query(FoodModel).filter(
            FoodModel.id == food_id
        ).first()

        if not food_model:
            return None

        restaurant = db.query(RestaurantModel).filter(
            RestaurantModel.id == restaurant_id
        ).first()

        if not restaurant:
            return None

        food = Food(
            food_id,
            name,
            price,
            category
        )

        food_model.name = food.name
        food_model.price = food.price
        food_model.category = food.category
        food_model.restaurant_id = restaurant_id

        db.commit()
        db.refresh(food_model)

        return food_model

    def delete_food(self, db, food_id):
        food_model = db.query(FoodModel).filter(
            FoodModel.id == food_id
        ).first()

        if not food_model:
            return None

        db.delete(food_model)
        db.commit()

        return True

    def get_restaurant_foods(self, db, restaurant_id):
        restaurant = db.query(RestaurantModel).filter(
            RestaurantModel.id == restaurant_id
        ).first()

        if not restaurant:
            return None

        foods = db.query(FoodModel).filter(
            FoodModel.restaurant_id == restaurant_id
        ).all()

        return foods