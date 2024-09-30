from pydantic import BaseModel, Field

#--------------------
class InfoCameraUpdate(BaseModel):
    fps: float = None
    width: int = None
    height: int = None

class InfoCamera(InfoCameraUpdate):
    id: str = Field(alias="_id")

#---------------------------
class CameraUpdate(BaseModel):
    name: str = None
    uri: str  = None
    is_active: bool = True
    task_id: str = None
    info: InfoCameraUpdate = None
    source_id : int = None

class Camera(CameraUpdate):
    id: str = Field(alias="_id")