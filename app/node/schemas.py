from pydantic import Field
import typing as tp

from pydantic import BaseModel


class NodeSchema(BaseModel):
    id: int = Field(..., title='Node_id')
    name: str = Field(..., title='Name')
    parent_id: tp.Optional[int] = Field(None, title='Parent id')

    class Config:
        orm_mode = True


class TreeSchema(BaseModel):
    parent: NodeSchema
    children: list[tp.Union[NodeSchema, "TreeSchema"]]


TreeSchema.update_forward_refs()


class NodeCreateSchema(BaseModel):
    name: str = Field(..., title='Name')
    parent_id: tp.Optional[int] = Field(None, title='Parent id')


class ResponseBool(BaseModel):
    result: bool = Field(True)
