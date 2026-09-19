from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.dependencies import get_db
from schemas.payment_schema import PaymentRequest
from services.payment_service import PaymentService


router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)

service = PaymentService()


@router.post("/")
def process_payment(
    request: PaymentRequest,
    db: Session = Depends(get_db)
):

    payment = service.process_payment(
        db,
        request.order_id,
        request.method
    )

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {
        "payment_id": payment.id,
        "order_id": payment.order_id,
        "amount": payment.amount,
        "method": payment.method,
        "status": payment.status
    }


@router.get("/")
def get_payments(
    db: Session = Depends(get_db)
):

    payments = service.get_payments(db)

    return [
        {
            "payment_id": payment.id,
            "order_id": payment.order_id,
            "amount": payment.amount,
            "method": payment.method,
            "status": payment.status
        }
        for payment in payments
    ]


@router.get("/{payment_id}")
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):

    payment = service.get_payment(
        db,
        payment_id
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return {
        "payment_id": payment.id,
        "order_id": payment.order_id,
        "amount": payment.amount,
        "method": payment.method,
        "status": payment.status
    }


@router.put("/{payment_id}/status")
def update_payment_status(
    payment_id: int,
    status: str,
    db: Session = Depends(get_db)
):

    payment = service.update_payment_status(
        db,
        payment_id,
        status
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return {
        "payment_id": payment.id,
        "status": payment.status
    }