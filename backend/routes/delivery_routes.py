from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.dependencies import get_db
from schemas.delivery_schema import DeliveryRequest
from services.delivery_service import DeliveryService


router = APIRouter(
    prefix="/deliveries",
    tags=["Deliveries"]
)

service = DeliveryService()


@router.post("/")
def create_delivery(
    request: DeliveryRequest,
    db: Session = Depends(get_db)
):

    delivery = service.create_delivery(
        db,
        request.order_id
    )

    if delivery is None:
        raise HTTPException(
            status_code=404,
            detail="Order or customer not found"
        )

    return {
        "delivery_id": delivery.id,
        "order_id": delivery.order_id,
        "address": delivery.address,
        "status": delivery.status
    }


@router.get("/")
def get_deliveries(
    db: Session = Depends(get_db)
):

    deliveries = service.get_deliveries(db)

    return [
        {
            "delivery_id": delivery.id,
            "order_id": delivery.order_id,
            "address": delivery.address,
            "status": delivery.status
        }
        for delivery in deliveries
    ]


@router.get("/{delivery_id}")
def get_delivery(
    delivery_id: int,
    db: Session = Depends(get_db)
):

    delivery = service.get_delivery(
        db,
        delivery_id
    )

    if not delivery:
        raise HTTPException(
            status_code=404,
            detail="Delivery not found"
        )

    return {
        "delivery_id": delivery.id,
        "order_id": delivery.order_id,
        "address": delivery.address,
        "status": delivery.status
    }


@router.put("/{delivery_id}/status")
def update_delivery_status(
    delivery_id: int,
    status: str,
    db: Session = Depends(get_db)
):

    delivery = service.update_delivery_status(
        db,
        delivery_id,
        status
    )

    if not delivery:
        raise HTTPException(
            status_code=404,
            detail="Delivery not found"
        )

    return {
        "delivery_id": delivery.id,
        "status": delivery.status
    }