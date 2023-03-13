from uuid import UUID

from fastapi import APIRouter

import kori.app.dao.organization as organization_dao
from kori.app.core.config import Settings
from kori.app.schemas.organization import OrganizationCreate, OrganizationSchema, OrganizationUpdate

organization_router = APIRouter()
config = Settings()


@organization_router.post("/", response_model=OrganizationSchema)
def create_organization(organization_create: OrganizationCreate) -> OrganizationSchema:
    return organization_dao.create(organization_create)


@organization_router.get("/{organization_id}", response_model=OrganizationSchema)
def get_organization_by_id(organization_id: UUID) -> OrganizationSchema:
    return organization_dao.get_organization_by_id(organization_id)


@organization_router.get("/", response_model=list[OrganizationSchema])
def get_all_organizations() -> list[OrganizationSchema]:
    return organization_dao.get_all_organizations()


@organization_router.put("/{organization_id}", response_model=OrganizationSchema)
def update_organization(organization_id: UUID, organization_update: OrganizationUpdate) -> OrganizationSchema:
    return organization_dao.update(organization_id, organization_update)


@organization_router.delete("/{organization_id}")
def delete_organization(organization_id: UUID):
    organization_dao.delete(organization_id)
    return "Deleted"
