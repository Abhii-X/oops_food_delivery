from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.dependencies import get_db
from services.customer_service import CustomerService


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

service = CustomerService()


@router.post("/")
def create_customer(
    name: str,
    email: str,
    phone: str,
    address: str,
    db: Session = Depends(get_db)
):
    customer = service.create_customer(
        db,
        name,
        email,
        phone,
        address
    )

    return {
        "id": customer.id,
        "name": customer.name,
        "email": customer.email,
        "phone": customer.phone,
        "address": customer.address
    }


@router.get("/")
def get_customers(
    db: Session = Depends(get_db)
):
    customers = service.get_customers(db)

    return [
        {
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "phone": customer.phone,
            "address": customer.address
        }
        for customer in customers
    ]


@router.get("/{customer_id}")
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = service.get_customer(
        db,
        customer_id
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return {
        "id": customer.id,
        "name": customer.name,
        "email": customer.email,
        "phone": customer.phone,
        "address": customer.address
    }


@router.put("/{customer_id}")
def update_customer(
    customer_id: int,
    name: str,
    email: str,
    phone: str,
    address: str,
    db: Session = Depends(get_db)
):
    customer = service.update_customer(
        db,
        customer_id,
        name,
        email,
        phone,
        address
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return {
        "id": customer.id,
        "name": customer.name,
        "email": customer.email,
        "phone": customer.phone,
        "address": customer.address
    }


@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    result = service.delete_customer(
        db,
        customer_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return {
        "message": "Customer deleted successfully"
    }