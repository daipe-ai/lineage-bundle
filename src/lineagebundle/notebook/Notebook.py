from datetime import datetime
from uuid import uuid4
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import String, DateTime
from sqlalchemybundle.entity.Base import Base


class Notebook(Base):
    __tablename__ = "notebook"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid4)
    label = Column(String(300), nullable=False)
    path = Column(String(500), nullable=False)
    layer = Column(String(100), nullable=False)
    created_at = Column(DateTime(), nullable=False)
    deleted_at = Column(DateTime(), nullable=True)

    def __init__(self, label: str, path: str, layer: str, created_at: DateTime = datetime.now()):
        self.label = label
        self.path = path
        self.layer = layer
        self.created_at = created_at

    def update(self, label: str, layer: str):
        self.label = label
        self.layer = layer
