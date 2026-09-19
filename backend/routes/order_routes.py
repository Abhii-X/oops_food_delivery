from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.dependencies import get_db
from schemas.order_schema import OrderCreateRequest
from services.order_service import OrderService


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

service = OrderService()


@router.post("/")
def create_order(
    request: OrderCreateRequest,
    db: Session = Depends(get_db)
):

    result = service.create_order(
        db,
        request.customer_id,
        request.items
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Customer or food not found"
        )

    order_model, order = result

    return {
        "order_id": order_model.id,
        "customer_id": order_model.customer_id,
        "status": order.status,
        "total": order.calculate_total()
    }


@router.get("/")
def get_orders(
    db: Session = Depends(get_db)
):

    orders = service.get_orders(db)

    result = []

    for order in orders:

        result.append({
            "order_id": order.id,
            "customer_id": order.customer_id,
            "status": order.status
        })

    return result


@router.get("/{order_id}")
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):

    order = service.get_order(
        db,
        order_id
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {
        "order_id": order.order_id,
        "customer_id": order.customer.email,
        "status": order.status,
        "total": order.calculate_total(),
        "items": [
            {
                "food_id": item.food.food_id,
                "food_name": item.food.name,
                "price": item.food.price,
                "quantity": item.quantity,
                "item_total": item.get_total()
            }
            for item in order.items
        ]
    }


@router.put("/{order_id}/status")
def update_order_status(
    order_id: int,
    status: str,
    db: Session = Depends(get_db)
):

    order = service.update_order_status(
        db,
        order_id,
        status
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {
        "order_id": order.id,
        "status": order.status
    }


@router.delete("/{order_id}")
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db)
):

    order = service.cancel_order(
        db,
        order_id
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {
        "order_id": order.id,
        "status": order.status
    }