from datetime import datetime
from typing import Union
from uuid import uuid4
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.sql.schema import Column
from sqlalchemy.types import String, DateTime
from sqlalchemybundle.entity.Base import Base


class Notebook(Base):
    __tablename__ = "notebook"

    id: Union[Column, str] = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid4)
    label: Union[Column, str] = Column(String(300), nullable=False)
    path: Union[Column, str] = Column(String(500), nullable=False)
    layer: Union[Column, str] = Column(String(100), nullable=False)
    created_at: Union[Column, datetime] = Column(DateTime(), nullable=False)
    deleted_at: Union[Column, datetime] = Column(DateTime(), nullable=True)

    def __init__(self, label: str, path: str, layer: str, created_at: datetime = datetime.now()):
        self.label = label
        self.path = path
        self.layer = layer
        self.created_at = created_at

    def update(self, label: str, layer: str):
        self.label = label
        self.layer = layer

    def __repr__(self):
        return f"{self.label}"
