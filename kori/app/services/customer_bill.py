from datetime import datetime
from uuid import UUID

import kori.app.dao.customer_bill as customer_bill_dao
import kori.app.dao.global_config as global_config_dao
from kori.app.schemas.customer_bill import CustomerBillCreate, CustomerBillDbCreate, CustomerBillSchema
from kori.app.schemas.product import ProductSchema
from kori.app.schemas.product_billed import ProductBilledDbCreate
from kori.app.services.product import get_product


def create_customer_bill(organization_id: UUID, bill_request: CustomerBillCreate) -> CustomerBillSchema:
    # get the latest versions of each product
    latest_products: list[ProductSchema] = [get_product(product.product_id) for product in bill_request.products_billed]
    product_billed_db_create_list: list[ProductBilledDbCreate] = []
    for bill_product, product_db in zip(bill_request.products_billed, latest_products):
        product_billed_db_create_list.append(
            ProductBilledDbCreate(
                product_id=product_db.product_id,
                version_id=product_db.version_id,
                total_cost=(bill_product.product_quantity * product_db.price),
                product_quantity=bill_product.product_quantity,
            )
        )

    products_total = sum(product.total_cost for product in product_billed_db_create_list)

    net_price = products_total - bill_request.discount_price + bill_request.delivery_charge
    billed_at = datetime.now()

    customer_bill_db_create = CustomerBillDbCreate(
        **bill_request.dict(exclude={"products_billed"}),
        products_total=products_total,
        net_price=net_price,
        billed_at=billed_at,
    )

    org_points_config = global_config_dao.get_config(organization_id, global_config_dao.POINTS_PERCENTAGE_CONFIG_TYPE)
    points = (products_total * float(org_points_config.value)) / 100.0

    return customer_bill_dao.create_customer_bill(customer_bill_db_create, product_billed_db_create_list, points)
