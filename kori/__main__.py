import uvicorn
from fastapi import FastAPI

from kori.app.core.config import Settings
from kori.app.routers.customer import customer_router

settings = Settings()

app = FastAPI(title=settings.APP_TITLE)

app.include_router(
    customer_router,
    prefix=f"/customer/v1",
    tags=["Customer API V1"],
)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)