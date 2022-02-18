from datetime import datetime
from typing import List, Optional, Union
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

    id: Union[Column, str] = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid4)
    name: Union[Column, str] = Column(String(100), nullable=False)
    notebook_id: Union[Column, str] = Column(UNIQUEIDENTIFIER, ForeignKey("notebook.id"), nullable=False)
    notebook = relationship(Notebook)
    input_datasets: Union[Column, List[str]] = Column(JSON, nullable=False)
    output_dataset: Union[Column, Optional[str]] = Column(String(100), nullable=True)
    created_at: Union[Column, datetime] = Column(DateTime(), nullable=False)
    deleted_at: Union[Column, datetime] = Column(DateTime(), nullable=True)

    def __init__(
        self,
        name: str,
        notebook: Notebook,
        input_datasets: List[str],
        output_dataset: Optional[str] = None,
        created_at: datetime = datetime.now(),
    ):
        self.name = name
        self.notebook = notebook
        self.input_datasets = input_datasets
        self.output_dataset = output_dataset
        self.created_at = created_at
