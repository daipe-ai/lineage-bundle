from datetime import datetime
from typing import Union
from uuid import uuid4
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.types import String, DateTime
from sqlalchemybundle.entity.Base import Base
from lineagebundle.notebook.Notebook import Notebook


class NotebookFunctionsRelation(Base):
    __tablename__ = "notebook_functions_relation"

    id: Union[Column, str] = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid4)
    notebook_id: Union[Column, str] = Column(UNIQUEIDENTIFIER, ForeignKey("notebook.id"), nullable=False)
    notebook = relationship(Notebook)
    source: Union[Column, str] = Column(String(100), nullable=False)
    target: Union[Column, str] = Column(String(100), nullable=False)
    created_at: Union[Column, datetime] = Column(DateTime(), nullable=False)
    deleted_at: Union[Column, datetime] = Column(DateTime(), nullable=True)

    def __init__(self, notebook: Notebook, source: str, target: str, created_at: datetime = datetime.now()):
        self.notebook = notebook
        self.source = source
        self.target = target
        self.created_at = created_at
