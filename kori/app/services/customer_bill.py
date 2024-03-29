from datetime import datetime
from uuid import UUID

import kori.app.dao.customer_bill as customer_bill_dao
import kori.app.dao.global_config as global_config_dao
import kori.app.dao.product as product_dao
from kori.app.core.exceptions import BadRequestException, ForbiddenException, NotFoundException
from kori.app.dao.customer import get_customer_by_id
from kori.app.schemas.customer_bill import (
    CustomerBillCreate,
    CustomerBillDbCreate,
    CustomerBillSchema,
    CustomerBillWithProducts,
)
from kori.app.schemas.product import ProductSchema
from kori.app.schemas.product_billed import ProductBilledDbCreate, ProductBilledWithProduct
from kori.app.services.product import get_product


def create_customer_bill(organization_id: UUID, bill_request: CustomerBillCreate) -> CustomerBillSchema:
    customer = get_customer_by_id(bill_request.customer_id)
    if not customer.is_member and bill_request.discount_price > 0:
        raise BadRequestException(message="Discount applicable to members only")

    if bill_request.discount_price > customer.membership_points:
        raise BadRequestException(message="Insufficient membership points for discount")

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

    free_delivery_config = global_config_dao.get_config(organization_id, global_config_dao.FREE_DELIVERY_CONFIG)

    if products_total > float(free_delivery_config.value) and bill_request.delivery_charge > 0:
        raise BadRequestException(message="Delivery charge not applicable")

    net_price = products_total - bill_request.discount_price + bill_request.delivery_charge
    billed_at = datetime.now()

    customer_bill_db_create = CustomerBillDbCreate(
        **bill_request.dict(exclude={"products_billed"}),
        products_total=products_total,
        net_price=net_price,
        billed_at=billed_at,
    )

    org_points_config = global_config_dao.get_config(organization_id, global_config_dao.POINTS_PERCENTAGE_CONFIG)
    points = (products_total * float(org_points_config.value)) / 100.0

    return customer_bill_dao.create_customer_bill(customer_bill_db_create, product_billed_db_create_list, points)


def get_customer_bill(organization_id: UUID, customer_bill_id: UUID) -> CustomerBillWithProducts:
    customer_bill = customer_bill_dao.get_customer_bill(customer_bill_id)

    if not customer_bill:
        raise NotFoundException()
    if customer_bill.org_id != organization_id:
        raise ForbiddenException()

    products_billed = customer_bill.products_billed
    products_billed_with_product = []
    for product_billed in products_billed:
        product = product_dao.get_product_by_version_id(product_billed.product_id, product_billed.version_id)
        products_billed_with_product.append(
            ProductBilledWithProduct(
                reorder_level=product.reorder_level,
                name=product.name,
                price=product.price,
                measurement_unit=product.measurement_unit,
                product_id=product.product_id,
                product_quantity=product_billed.product_quantity,
                total_cost=product_billed.total_cost,
                version_id=product_billed.version_id,
            )
        )

    return CustomerBillWithProducts(
        org_id=organization_id,
        store_id=customer_bill.store_id,
        customer_id=customer_bill.customer_id,
        user_id=customer_bill.user_id,
        payment_method=customer_bill.payment_method,
        discount_price=customer_bill.discount_price,
        delivery_address=customer_bill.delivery_address,
        delivery_charge=customer_bill.delivery_charge,
        products_total=customer_bill.products_total,
        net_price=customer_bill.net_price,
        billed_at=customer_bill.billed_at,
        id=customer_bill.id,
        products_billed=products_billed_with_product,
    )
