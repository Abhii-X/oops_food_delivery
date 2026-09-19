from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.dependencies import get_db
from services.restaurant_service import RestaurantService


router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"]
)

service = RestaurantService()


@router.post("/")
def create_restaurant(
    name: str,
    address: str,
    db: Session = Depends(get_db)
):
    restaurant = service.create_restaurant(
        db,
        name,
        address
    )

    return {
        "id": restaurant.id,
        "name": restaurant.name,
        "address": restaurant.address
    }


@router.get("/")
def get_restaurants(
    db: Session = Depends(get_db)
):
    restaurants = service.get_restaurants(db)

    return [
        {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address
        }
        for restaurant in restaurants
    ]


@router.get("/{restaurant_id}")
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    restaurant = service.get_restaurant(
        db,
        restaurant_id
    )

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    return {
        "id": restaurant.id,
        "name": restaurant.name,
        "address": restaurant.address
    }


@router.put("/{restaurant_id}")
def update_restaurant(
    restaurant_id: int,
    name: str,
    address: str,
    db: Session = Depends(get_db)
):
    restaurant = service.update_restaurant(
        db,
        restaurant_id,
        name,
        address
    )

    if not restaurant:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    return {
        "id": restaurant.id,
        "name": restaurant.name,
        "address": restaurant.address
    }


@router.delete("/{restaurant_id}")
def delete_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    result = service.delete_restaurant(
        db,
        restaurant_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    return {
        "message": "Restaurant deleted successfully"
    }