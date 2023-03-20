from datetime import datetime

from kori.app.core.config import Settings
from kori.app.db.connection import DbConnector
from kori.app.models import (
    Customer,
    CustomerBill,
    GlobalConfig,
    Product,
    ProductBilled,
    ProductVersion,
    Store,
    StoreProduct,
    User,
    Warehouse,
    WarehouseProduct,
)
from kori.app.models.organization import Organization
from kori.app.schemas.user import PermissionLevel

if __name__ == "__main__":
    config = Settings()
    connector = DbConnector(config.DATABASE_URI)
    session = connector.get_session()

    org = Organization(name="test-org")
    session.add(org)
    session.commit()
    org_id = org.id

    gc = GlobalConfig(org_id=org_id, config_type="key", value="val")
    session.add(gc)
    session.commit()

    store = Store(org_id=org_id, name="Test Store")
    session.add(store)
    session.commit()
    store_id = store.id

    warehouse = Warehouse(org_id=org_id, name="Test Warehouse")
    session.add(warehouse)
    session.commit()
    warehouse_id = warehouse.id

    user = User(
        org_id=org_id,
        name="Test User",
        email="test@email.com",
        permission_level=PermissionLevel.user,
        pass_hash=b"Test",
    )
    session.add(user)
    session.commit()
    user_id = user.id

    customer = Customer(
        org_id=org_id,
        name="Test User",
        email="test@email.com",
        phone_number="+911234567890",
        is_member=False,
        membership_points=0,
        address="Test Address",
        preferred_payment_method="Test",
    )
    session.add(customer)
    session.commit()
    customer_id = customer.id

    product = Product(org_id=org_id, reorder_level=10)
    session.add(product)
    session.commit()
    product_id = product.id

    warehouse_product = WarehouseProduct(warehouse_id=warehouse_id, product_id=product_id, stock_available=20)
    session.add(warehouse_product)
    session.commit()

    store_product = StoreProduct(store_id=store_id, product_id=product_id, stock_available=20, stock_locked=5)
    session.add(store_product)
    session.commit()

    product_version = ProductVersion(
        product_id=product_id,
        version_id=1,
        name="Tomato",
        price=20,
        valid_from=datetime.now(),
        valid_to=datetime.now(),
        measurement_unit="Test",
    )
    session.add(product_version)
    session.commit()
    pv_id = product_version.version_id

    customer_bill = CustomerBill(
        org_id=org_id,
        store_id=store_id,
        customer_id=customer_id,
        user_id=user_id,
        payment_method="Test",
        products_total=50,
        discount_price=50,
        delivery_address="Test",
        delivery_charge=0,
        net_price=50,
        billed_at=datetime.now(),
    )
    session.add(customer_bill)
    session.commit()
    cb_id = customer_bill.id

    product_billed = ProductBilled(
        product_id=product_id,
        customer_bill_id=cb_id,
        product_quantity=1,
        version_id=pv_id,
        total_cost=50,
    )
    session.add(product_billed)
    session.commit()

    # Delete created objects
    session.delete(product_billed)
    session.delete(customer_bill)
    session.delete(product_version)
    session.delete(store_product)
    session.delete(warehouse_product)
    session.delete(product)
    session.delete(customer)
    session.delete(user)
    session.delete(warehouse)
    session.delete(store)
    session.delete(gc)
    session.delete(org)

    session.commit()
