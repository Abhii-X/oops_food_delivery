from models.customer import Customer
from database.customer_model import CustomerModel


class CustomerService:

    def create_customer(self, db, name, email, phone, address):
        customer = Customer(
            name,
            email,
            phone,
            address
        )

        customer_model = CustomerModel(
            name=customer.name,
            email=customer.email,
            phone=customer.phone,
            address=customer.address
        )

        db.add(customer_model)
        db.commit()
        db.refresh(customer_model)

        return customer_model

    def get_customers(self, db):
        return db.query(CustomerModel).all()

    def get_customer(self, db, customer_id):
        return db.query(CustomerModel).filter(
            CustomerModel.id == customer_id
        ).first()

    def update_customer(
        self,
        db,
        customer_id,
        name,
        email,
        phone,
        address
    ):
        customer_model = db.query(CustomerModel).filter(
            CustomerModel.id == customer_id
        ).first()

        if not customer_model:
            return None

        customer = Customer(
            name,
            email,
            phone,
            address
        )

        customer_model.name = customer.name
        customer_model.email = customer.email
        customer_model.phone = customer.phone
        customer_model.address = customer.address

        db.commit()
        db.refresh(customer_model)

        return customer_model

    def delete_customer(self, db, customer_id):
        customer_model = db.query(CustomerModel).filter(
            CustomerModel.id == customer_id
        ).first()

        if not customer_model:
            return None

        db.delete(customer_model)
        db.commit()

        return True