from uuid import UUID

from fastapi import APIRouter

import kori.app.dao.global_config as global_config_dao
from kori.app.core.config import Settings
from kori.app.core.exceptions import ForbiddenException, NotFoundException
from kori.app.schemas.global_config import GlobalConfigCreate, GlobalConfigSchema

global_config_router = APIRouter()
config = Settings()

BASE = "/{organization_id}"


@global_config_router.post(BASE, response_model=GlobalConfigSchema)
def create_global_config(organization_id: UUID, config_create: GlobalConfigCreate) -> GlobalConfigSchema:
    if organization_id != config_create.org_id:
        raise ForbiddenException()

    return global_config_dao.set_config(config_create)


@global_config_router.get(BASE + "/{config_type}", response_model=GlobalConfigSchema)
def create_global_config(organization_id: UUID, config_type: str) -> GlobalConfigSchema:
    global_config = global_config_dao.get_config(organization_id, config_type)
    if global_config is None:
        raise NotFoundException()
    return global_config
