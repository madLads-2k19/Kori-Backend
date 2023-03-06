from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


class DbConnector:
    def __init__(self, database_uri: str):
        self.engine: Engine = create_engine(database_uri)

    def get_session(self) -> Session:
        session = Session(autocommit=False, autoflush=False, bind=self.engine)
        return session
