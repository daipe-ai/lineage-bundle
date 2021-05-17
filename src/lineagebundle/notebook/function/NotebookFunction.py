from datetime import datetime
from typing import List
from uuid import uuid4
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.types import String, DateTime, JSON
from sqlalchemybundle.entity.Base import Base
from lineagebundle.notebook.Notebook import Notebook


class NotebookFunction(Base):
    __tablename__ = "notebook_function"
    __table_args__ = (UniqueConstraint("name", "notebook_id", name="node_name_notebook_id_unique"),)

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
    notebook_id = Column(UNIQUEIDENTIFIER, ForeignKey("notebook.id"), nullable=False)
    notebook = relationship(Notebook)
    input_tables = Column(JSON, nullable=False)
    output_table = Column(String(100), nullable=True)
    created_at = Column(DateTime(), nullable=False)

    def __init__(self, name: str, notebook: Notebook, input_tables: List[str], output_table: str = None):
        self.name = name
        self.notebook = notebook
        self.input_tables = input_tables
        self.output_table = output_table
        self.created_at = datetime.now()
