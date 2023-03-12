from uuid import UUID

from pydantic import BaseModel


class OrganizationCreate(BaseModel):
    name: str


class OrganizationUpdate(BaseModel):
    name: str


class OrganizationDelete(BaseModel):
    id: UUID


class OrganizationSchema(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True
