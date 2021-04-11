from datetime import datetime
from uuid import uuid4
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, UniqueConstraint, ForeignKey
from sqlalchemy.types import DateTime
from sqlalchemybundle.entity.Base import Base
from lineagebundle.pipeline.Notebook import Notebook


class NotebooksRelation(Base):
    __tablename__ = "notebooks_relation"
    __table_args__ = (UniqueConstraint("source_id", "target_id", name="notebooks_relation_unique"),)

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid4)
    source_id = Column(UNIQUEIDENTIFIER, ForeignKey("notebook.id"), nullable=False)
    source = relationship(Notebook, foreign_keys=[source_id])
    target_id = Column(UNIQUEIDENTIFIER, ForeignKey("notebook.id"), nullable=False)
    target = relationship(Notebook, foreign_keys=[target_id])
    created_at = Column(DateTime(), nullable=False)

    def __init__(self, source: Notebook, target: Notebook):
        self.source = source
        self.target = target
        self.created_at = datetime.now()
