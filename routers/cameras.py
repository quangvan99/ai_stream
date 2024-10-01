from fastapi import APIRouter, HTTPException
from bson import ObjectId
import threading

from database import db
from models.cameras import CameraUpdate
from utils import parse_json
from pipeline import pipeline   # create base pipeline here

router = APIRouter() 

@router.get("/cameras")
async def get_cameras():
    cameras = await db.cameras.find().to_list(length=100)
    return [parse_json(camera) for camera in cameras]

@router.post("/cameras")
async def create_camera(manager_id: str, task_id : str, new_camera: CameraUpdate):
    manager = await db.managers.find_one({"_id": ObjectId(manager_id)})
    if not manager:
        raise HTTPException(status_code=400, detail="Manager not found")
    
    task = await db.tasks.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=400, detail="Task not found")
    
    # Add camera to task
    threading.Thread(target=pipeline.add_cam, args=(len(task["cameras"]), new_camera.uri)).start()

    new_camera.task_id = task_id
    new_camera.source_id = len(task["cameras"]) # source_id is the index of camera in the task

    camera = await db.cameras.insert_one(new_camera.model_dump(by_alias=True))

    await db.tasks.update_one({"_id": ObjectId(task_id)},{"$push": {"cameras": str(camera.inserted_id)}})

    return {"message": "Camera created successfully"}

@router.get("/cameras/{camera_id}")
async def read_camera(manager_id: str, task_id : str, camera_id):
    manager = await db.managers.find_one({"_id": ObjectId(manager_id)})
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")
    
    task = await db.tasks.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    camera = await db.cameras.find_one({"_id": ObjectId(camera_id)})
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    
    return parse_json(camera)

@router.put("/cameras/{camera_id}")
async def update_camera(manager_id: str, task_id : str, camera_id: str, new_camera: CameraUpdate):
    manager = await db.managers.find_one({"_id": ObjectId(manager_id)})
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")
    
    task = await db.tasks.find_one({"_id": ObjectId(task_id)}) 
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    camera = await db.cameras.find_one({"_id": ObjectId(camera_id)})
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    
    # Update camera here
    source_id = camera["source_id"]
    threading.Thread(target=pipeline.change_cam, args=(source_id, new_camera.uri)).start()

    
    await db.cameras.update_one({"_id": ObjectId(camera_id)},{"$set": new_camera.model_dump(by_alias=True, exclude_none=True, exclude_defaults=True)})

    return {"message": "Camera updated successfully"}

@router.delete("/cameras/{camera_id}")
async def delete_camera(manager_id: str, task_id : str, camera_id):
    manager = await db.managers.find_one({"_id": ObjectId(manager_id)})
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")
    
    task = await db.tasks.find_one({"_id": ObjectId(task_id)})
    if not task_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    camera = await db.cameras.find_one({"_id": ObjectId(camera_id)})
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")

    # Delete camera
    source_id = camera["source_id"]
    threading.Thread(target=pipeline.delete_cam, args=(source_id, )).start()

    await db.cameras.delete_one({"_id": ObjectId(camera_id)})
    await db.tasks.update_one({"_id": ObjectId(task_id)},{"$pull": {"cameras": str(camera_id)}})

    return {"message": "Camera deleted successfully"}
