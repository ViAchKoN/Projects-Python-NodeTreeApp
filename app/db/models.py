import sqlalchemy as sa
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import attribute_mapped_collection

from app.db.base import Base


class Node(Base):
    __tablename__ = 'node'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(128), nullable=False)
    parent_id = sa.Column(sa.Integer, sa.ForeignKey("node.id"), nullable=True)
    children = relationship("Node", cascade='all', )
