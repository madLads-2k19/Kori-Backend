from typing import Any

from sqlalchemy.orm import as_declarative, declared_attr

from kori.app.core.util import camel_to_snake


@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        # Generate __tablename__ automatically
        return camel_to_snake(cls.__name__)
