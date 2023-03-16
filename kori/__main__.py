import uvicorn
from fastapi import FastAPI

from kori.app.core.config import Settings
from kori.app.routers.customer import customer_router
from kori.app.routers.customer_bill import customer_bill_router
from kori.app.routers.global_config import global_config_router
from kori.app.routers.organization import organization_router
from kori.app.routers.product import product_router
from kori.app.routers.store import store_router
from kori.app.routers.store_product import store_product_router
from kori.app.routers.user import user_router

config = Settings()

app = FastAPI(title=config.APP_TITLE)

app.include_router(
    customer_router,
    prefix="/customer/v1",
    tags=["Customer API V1"],
)
app.include_router(
    product_router,
    prefix="/product/v1",
    tags=["Product API V1"],
)

app.include_router(
    organization_router,
    prefix="/organization/v1",
    tags=["Organization API V1"],
)

app.include_router(
    store_router,
    prefix="/store/v1",
    tags=["Store API V1"],
)

app.include_router(
    store_product_router,
    prefix="/store_product/v1",
    tags=["Store Product API V1"],
)

app.include_router(
    user_router,
    prefix="/store/v1",
    tags=["Store API V1"],
)

app.include_router(customer_bill_router, prefix="/customer_bill/v1", tags=["Customer Bill API V1"])

app.include_router(global_config_router, prefix="/global_config/v1", tags=["Global Config API V1"])

app.include_router(user_router, prefix="/user/v1", tags=["User API V1"])

if __name__ == "__main__":
    uvicorn.run(app, host=config.SERVER_HOST, port=config.SERVER_PORT)
