from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.dependencies import get_db
from services.food_service import FoodService


router = APIRouter(
    prefix="/foods",
    tags=["Foods"]
)

service = FoodService()


@router.post("/")
def create_food(
    name: str,
    price: float,
    category: str,
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    food = service.create_food(
        db,
        name,
        price,
        category,
        restaurant_id
    )

    if not food:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    return {
        "id": food.id,
        "name": food.name,
        "price": food.price,
        "category": food.category,
        "restaurant_id": food.restaurant_id
    }


@router.get("/")
def get_foods(
    db: Session = Depends(get_db)
):
    foods = service.get_foods(db)

    return [
        {
            "id": food.id,
            "name": food.name,
            "price": food.price,
            "category": food.category,
            "restaurant_id": food.restaurant_id
        }
        for food in foods
    ]


@router.get("/restaurant/{restaurant_id}")
def get_restaurant_foods(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    foods = service.get_restaurant_foods(
        db,
        restaurant_id
    )

    if foods is None:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    return [
        {
            "id": food.id,
            "name": food.name,
            "price": food.price,
            "category": food.category,
            "restaurant_id": food.restaurant_id
        }
        for food in foods
    ]


@router.get("/{food_id}")
def get_food(
    food_id: int,
    db: Session = Depends(get_db)
):
    food = service.get_food(
        db,
        food_id
    )

    if not food:
        raise HTTPException(
            status_code=404,
            detail="Food not found"
        )

    return {
        "id": food.id,
        "name": food.name,
        "price": food.price,
        "category": food.category,
        "restaurant_id": food.restaurant_id
    }


@router.put("/{food_id}")
def update_food(
    food_id: int,
    name: str,
    price: float,
    category: str,
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    food = service.update_food(
        db,
        food_id,
        name,
        price,
        category,
        restaurant_id
    )

    if not food:
        raise HTTPException(
            status_code=404,
            detail="Food or restaurant not found"
        )

    return {
        "id": food.id,
        "name": food.name,
        "price": food.price,
        "category": food.category,
        "restaurant_id": food.restaurant_id
    }


@router.delete("/{food_id}")
def delete_food(
    food_id: int,
    db: Session = Depends(get_db)
):
    result = service.delete_food(
        db,
        food_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Food not found"
        )

    return {
        "message": "Food deleted successfully"
    }


@router.get("/restaurant/{restaurant_id}")
def get_restaurant_foods(
    restaurant_id: int,
    db: Session = Depends(get_db)
):
    foods = service.get_restaurant_foods(
        db,
        restaurant_id
    )

    if foods is None:
        raise HTTPException(
            status_code=404,
            detail="Restaurant not found"
        )

    return [
        {
            "id": food.id,
            "name": food.name,
            "price": food.price,
            "category": food.category,
            "restaurant_id": food.restaurant_id
        }
        for food in foods
    ]