from pydantic import BaseModel, Field
from typing import List
from .cameras import CameraUpdate

#---------------------------
class TaskUpdate(BaseModel):
    name: str = None
    is_active: bool = False
    str_pipeline: dict = None
    cameras: List[CameraUpdate] = []
    manager_id: str = None

class Task(TaskUpdate):
    id: str = Field(alias="_id")