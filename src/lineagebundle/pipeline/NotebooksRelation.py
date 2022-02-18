from datetime import datetime
from typing import Union
from uuid import uuid4
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.types import DateTime
from sqlalchemybundle.entity.Base import Base
from lineagebundle.notebook.Notebook import Notebook


class NotebooksRelation(Base):
    __tablename__ = "notebooks_relation"
    __table_args__ = (UniqueConstraint("source_id", "target_id", name="notebooks_relation_unique"),)

    id: Union[Column, str] = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid4)
    source_id: Union[Column, str] = Column(UNIQUEIDENTIFIER, ForeignKey("notebook.id"), nullable=False)
    source = relationship(Notebook, foreign_keys=[source_id])
    target_id: Union[Column, str] = Column(UNIQUEIDENTIFIER, ForeignKey("notebook.id"), nullable=False)
    target = relationship(Notebook, foreign_keys=[target_id])
    created_at: Union[Column, datetime] = Column(DateTime(), nullable=False)
    deleted_at: Union[Column, datetime] = Column(DateTime(), nullable=True)

    def __init__(self, source: Notebook, target: Notebook, created_at: datetime = datetime.now()):
        self.source = source
        self.target = target
        self.created_at = created_at
