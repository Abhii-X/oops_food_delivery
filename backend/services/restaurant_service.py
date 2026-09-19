from models.restaurant import Restaurant
from database.restaurant_model import RestaurantModel


class RestaurantService:

    def create_restaurant(self, db, name, address):
        restaurant = Restaurant(
            0,
            name,
            address
        )

        restaurant_model = RestaurantModel(
            name=restaurant.name,
            address=restaurant.address
        )

        db.add(restaurant_model)
        db.commit()
        db.refresh(restaurant_model)

        return restaurant_model

    def get_restaurants(self, db):
        return db.query(RestaurantModel).all()

    def get_restaurant(self, db, restaurant_id):
        return db.query(RestaurantModel).filter(
            RestaurantModel.id == restaurant_id
        ).first()

    def update_restaurant(
        self,
        db,
        restaurant_id,
        name,
        address
    ):
        restaurant_model = db.query(RestaurantModel).filter(
            RestaurantModel.id == restaurant_id
        ).first()

        if not restaurant_model:
            return None

        restaurant = Restaurant(
            restaurant_id,
            name,
            address
        )

        restaurant_model.name = restaurant.name
        restaurant_model.address = restaurant.address

        db.commit()
        db.refresh(restaurant_model)

        return restaurant_model

    def delete_restaurant(self, db, restaurant_id):
        restaurant_model = db.query(RestaurantModel).filter(
            RestaurantModel.id == restaurant_id
        ).first()

        if not restaurant_model:
            return None

        db.delete(restaurant_model)
        db.commit()

        return True