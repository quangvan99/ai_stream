from pydantic import BaseModel, Field
from typing import List
from .tasks import TaskUpdate

class ManagerUpdate(BaseModel):
    name: str = None
    description: str = None
    is_active: bool = False
    tasks: List[TaskUpdate] = []

class Manager(ManagerUpdate):
    id: str = Field(alias="_id")
