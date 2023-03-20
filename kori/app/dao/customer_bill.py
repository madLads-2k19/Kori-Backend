import decimal
from uuid import UUID, uuid4

from kori.app.core.config import Settings
from kori.app.core.exceptions import StockLevelException
from kori.app.db.connection import DbConnector
from kori.app.models import Customer, CustomerBill, ProductBilled, StoreProduct
from kori.app.models.reorder import Reorder
from kori.app.schemas.customer_bill import CustomerBillDbCreate, CustomerBillSchema
from kori.app.schemas.product_billed import ProductBilledDbCreate, ProductBilledSchema

settings = Settings()
REORDER_FACTOR = 2

db_connector = DbConnector(settings.DATABASE_URI)


def create_customer_bill(
    customer_bill_db_create: CustomerBillDbCreate,
    product_billed_db_create_list: list[ProductBilledDbCreate],
    points: float,
):
    session = db_connector.get_session()
    with session.begin() as transaction:
        # Insert the bill
        customer_bill_id = uuid4()
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

            billed_quantity_decimal = decimal.Decimal(product_billed_create.product_quantity)
            if billed_quantity_decimal > store_product_db.stock_available:
                raise StockLevelException()
            store_product_db.stock_available -= billed_quantity_decimal

            if (
                store_product_db.stock_available <= store_product_db.product.reorder_level
                and not store_product_db.reorder_placed
            ):
                reorder_entry = Reorder(
                    org_id=customer_bill_db_create.org_id,
                    store_id=customer_bill_db_create.store_id,
                    product_id=product_billed_create.product_id,
                    reorder_quantity=(REORDER_FACTOR * store_product_db.product.reorder_level),
                    reorder_time=customer_bill_db_create.billed_at,
                    supplier_paid=False,
                )
                session.add(reorder_entry)
                store_product_db.reorder_placed = True

        # Increment customer membership points
        customer_db: Customer = session.query(Customer).get(customer_bill_db_create.customer_id)
        if customer_db.is_member:
            customer_db.membership_points += points

        transaction.commit()

    created_customer_bill = CustomerBillSchema.from_orm(customer_bill_db)
    session.close()
    return created_customer_bill


def get_customer_bill(customer_bill_id: UUID) -> CustomerBillSchema | None:
    session = db_connector.get_session()
    customer_bill = session.query(CustomerBill).get(customer_bill_id)
    customer_bill_schema = CustomerBillSchema.from_orm(customer_bill) if customer_bill else None
    session.close()
    return customer_bill_schema
