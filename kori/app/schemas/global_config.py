from uuid import UUID

from pydantic import BaseModel


class GlobalConfigBase(BaseModel):
    config_type: str
    value: str
    org_id: UUID


class GlobalConfigCreate(GlobalConfigBase):
    pass


class GlobalConfigSchema(GlobalConfigBase):
    id: UUID

    class Config:
        orm_mode = True
