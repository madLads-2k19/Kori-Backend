from uuid import UUID

from kori.app.core.config import Settings
from kori.app.core.exceptions import NotFoundException
from kori.app.db.connection import DbConnector
from kori.app.models.organization import Organization
from kori.app.schemas.organization import OrganizationCreate, OrganizationSchema, OrganizationUpdate
from kori.app.utils.dict_utils import remove_null_values

config = Settings()

db_connector = DbConnector(config.DATABASE_URI)


def create(organization_create: OrganizationCreate) -> OrganizationSchema:
    session = db_connector.get_session()
    new_org_db = Organization(**organization_create.dict())

    session.add(new_org_db)
    session.commit()

    return OrganizationSchema.from_orm(new_org_db)


def get_organization_by_id(organization_id: UUID) -> OrganizationSchema:
    session = db_connector.get_session()
    organization = session.query(Organization).get(organization_id)

    if organization is None:
        raise NotFoundException()

    return OrganizationSchema.from_orm(organization)


def get_all_organizations() -> list[OrganizationSchema]:
    session = db_connector.get_session()
    organizations = list(session.query(Organization))
    return [OrganizationSchema.from_orm(org) for org in organizations]


def update(organization_id: UUID, organization_update: OrganizationUpdate) -> OrganizationSchema:
    session = db_connector.get_session()
    update_data = remove_null_values(organization_update.dict())

    updated_count = session.query(Organization).filter(Organization.id == organization_id).update(update_data)
    session.commit()

    if updated_count == 0:
        raise NotFoundException(message="No records matched for update")

    return get_organization_by_id(organization_id)


def delete(organization_id: UUID) -> None:
    session = db_connector.get_session()
    deleted_count = session.query(Organization).filter(Organization.id == organization_id).delete()
    session.commit()

    if deleted_count == 0:
        raise NotFoundException(message="No records matched for delete")
