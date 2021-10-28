import typing as tp

from sqlalchemy import func
from sqlalchemy.future import select

from app.db.models import Node


class NodeCrud:
    def __init__(self, db):
        self.db = db

    async def get_tree(self, node: Node):
        query = await self.db.execute(select(Node).filter(Node.parent_id == node.id))
        await self.db.commit()
        children = query.scalars().all()
        res = {'parent': node, 'children': []}
        for child in children:
            res['children'].append(await self.get_tree(child))
        else:
            return res

    async def get_node_by_id(
            self,
            node_id: int,
    ) -> tp.Optional[Node]:
        query = await self.db.execute(select(Node).filter(Node.id == node_id))
        await self.db.commit()
        return query.scalars().first()

    async def get_node_by_parent_id(
            self,
            parent_id: tp.Union[int, None],
    ) -> tp.Optional[Node]:
        query = await self.db.execute(select(Node).filter(Node.parent_id == parent_id))
        await self.db.commit()
        return query.scalars().first()

    async def get_max_id(
            self,
    ) -> int:
        query = await self.db.execute(func.max(Node.id))
        return query.scalar()

    async def create_node(
            self,
            node: Node,
    ) -> Node:
        self.db.add(node)
        await self.db.commit()
        await self.db.refresh(node)
        return node

    async def delete_node(
            self,
            node: Node,
    ):
        await self.db.delete(node)
        await self.db.commit()
