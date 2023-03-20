from uuid import UUID

from sqlalchemy.exc import IntegrityError

from kori.app.core.config import Settings
from kori.app.core.exceptions import DuplicateRecordException
from kori.app.db.connection import DbConnector
from kori.app.models import GlobalConfig
from kori.app.schemas.global_config import GlobalConfigCreate, GlobalConfigSchema

config = Settings()

db_connector = DbConnector(config.DATABASE_URI)


POINTS_PERCENTAGE_CONFIG = "BILL_POINTS_PERCENT"
FREE_DELIVERY_CONFIG = "FREE_DELIVERY_BILL_VALUE"

DEFAULTS = {POINTS_PERCENTAGE_CONFIG: 5, FREE_DELIVERY_CONFIG: 1000}


def set_config(global_config_create: GlobalConfigCreate) -> GlobalConfigSchema:
    session = db_connector.get_session()
    new_config_db = GlobalConfig(**global_config_create.dict())

    try:
        session.add(new_config_db)
        session.commit()
    except IntegrityError:
        raise DuplicateRecordException(message="Global config entry with same key exists")

    return GlobalConfigSchema.from_orm(new_config_db)


def get_config(organization_id: UUID, config_type: str) -> GlobalConfigSchema | None:
    session = db_connector.get_session()
    matching_config = (
        session.query(GlobalConfig)
        .filter(GlobalConfig.org_id == organization_id, GlobalConfig.config_type == config_type)
        .one_or_none()
    )
    if matching_config is None and config_type in DEFAULTS:
        return GlobalConfigSchema(
            id=UUID("0" * 32), org_id=organization_id, config_type=config_type, value=DEFAULTS[config_type]
        )
    return GlobalConfigSchema.from_orm(matching_config) if matching_config else None
