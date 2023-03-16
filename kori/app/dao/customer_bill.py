import decimal
import uuid

from kori.app.core.config import Settings
from kori.app.db.connection import DbConnector
from kori.app.models import Customer, CustomerBill, ProductBilled, StoreProduct
from kori.app.schemas.customer_bill import CustomerBillDbCreate, CustomerBillSchema
from kori.app.schemas.product_billed import ProductBilledDbCreate

settings = Settings()

db_connector = DbConnector(settings.DATABASE_URI)
session = db_connector.get_session()


def create_customer_bill(
    customer_bill_db_create: CustomerBillDbCreate,
    product_billed_db_create_list: list[ProductBilledDbCreate],
    points: float,
):
    with session.begin() as transaction:
        # Insert the bill
        customer_bill_id = uuid.uuid4()
        customer_bill_db = CustomerBill(**customer_bill_db_create.dict(), id=customer_bill_id)
        session.add(customer_bill_db)

        for product_billed_create in product_billed_db_create_list:
            # Add the corresponding ProductBilled entries
            product_billed_db = ProductBilled(**product_billed_create.dict(), customer_bill_id=customer_bill_id)
            session.add(product_billed_db)

            # Update the inventory
            store_product_db: StoreProduct = session.query(StoreProduct).get(
                (product_billed_create.product_id, customer_bill_db_create.store_id)
            )
            store_product_db.stock_available -= decimal.Decimal(product_billed_create.product_quantity)

        # Increment customer membership points
        customer_db: Customer = session.query(Customer).get(customer_bill_db_create.customer_id)
        if customer_db.is_member:
            customer_db.membership_points += points

        transaction.commit()

    return CustomerBillSchema.from_orm(customer_bill_db)