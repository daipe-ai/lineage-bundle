from datetime import datetime
from uuid import uuid4
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.types import String, DateTime
from sqlalchemybundle.entity.Base import Base
from lineagebundle.pipeline.Notebook import Notebook


class LineageNode(Base):
    __tablename__ = "notebook_lineage_node"
    __table_args__ = (UniqueConstraint("name", "notebook_id", name="node_name_notebook_id_unique"),)

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
    notebook_id = Column(UNIQUEIDENTIFIER, ForeignKey("notebook.id"), nullable=False)
    notebook = relationship(Notebook)
    input_table = Column(String(100), nullable=True)
    output_table = Column(String(100), nullable=True)
    created_at = Column(DateTime(), nullable=False)

    def __init__(self, name: str, notebook: Notebook, input_table: str = None, output_table: str = None):
        self.name = name
        self.notebook = notebook
        self.input_table = input_table
        self.output_table = output_table
        self.created_at = datetime.now()
