from datetime import datetime
from uuid import uuid4
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.types import String, DateTime
from sqlalchemybundle.entity.Base import Base
from lineagebundle.notebook.Notebook import Notebook


class NotebookFunctionsRelation(Base):
    __tablename__ = "notebook_functions_relation"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid4)
    notebook_id = Column(UNIQUEIDENTIFIER, ForeignKey("notebook.id"), nullable=False)
    notebook = relationship(Notebook)
    source = Column(String(100), nullable=False)
    target = Column(String(100), nullable=False)
    created_at = Column(DateTime(), nullable=False)
    deleted_at = Column(DateTime(), nullable=True)

    def __init__(self, notebook: Notebook, source: str, target: str, created_at: DateTime = datetime.now()):
        self.notebook = notebook
        self.source = source
        self.target = target
        self.created_at = created_at
