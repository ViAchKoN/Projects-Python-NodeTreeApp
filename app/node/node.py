from fastapi import APIRouter, Depends
from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import typing as tp

from app.db import get_db, models
from app.node import schemas
from app.node.crud import NodeCrud
from app.node.schemas import TreeSchema, ResponseBool

node_router = APIRouter(
    prefix='/api/v1',
    tags=['node'],
)


@node_router.post(
    '/node',
    summary='Add nodes to the tree',
    responses={
        200: {"model": ResponseBool},
    },
)
async def create_node(
        nodes_to_create: list[schemas.NodeCreateSchema],
        db: AsyncSession = Depends(get_db),
):
    node_crud = NodeCrud(db=db)
    for new_node in nodes_to_create:
        parent_id = new_node.parent_id
        parent_node = await node_crud.get_node_by_id(node_id=parent_id)
        if (not parent_id and parent_node) or not parent_node:
            parent_id = await node_crud.get_max_id()
        new_node = models.Node(
            name=new_node.name,
            parent_id=parent_id
        )
        await node_crud.create_node(node=new_node)
    return JSONResponse(
        {'result': True},
        status_code=status.HTTP_200_OK,
    )


@node_router.get(
    '/tree',
    summary='Get the tree',
    response_model=TreeSchema,
)
async def get_tree(
        node_id: tp.Optional[int] = None,
        db: AsyncSession = Depends(get_db),
):
    node_crud = NodeCrud(db=db)
    if node_id:
        node = await node_crud.get_node_by_id(node_id=node_id)
        if not node:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Node with id {node_id} does not exists',
            )
    else:
        node = await node_crud.get_node_by_parent_id(parent_id=None)
    tree = await NodeCrud(db=db).get_tree(node)
    return tree


@node_router.delete(
    '/node/{node_id}',
    summary='Delete a node',
    responses={
        200: {"model": ResponseBool},
    },
)
async def delete_node(
        node_id: int,
        db: AsyncSession = Depends(get_db),
):
    node_crud = NodeCrud(db=db)
    node = await node_crud.get_node_by_id(node_id)
    if not node:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Node with id {node_id} does not exists',
        )
    await node_crud.delete_node(node=node)
    return JSONResponse(
        {'result': True},
        status_code=status.HTTP_200_OK,
    )
