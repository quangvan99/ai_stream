from fastapi import APIRouter, HTTPException
from bson import ObjectId
import threading

from database import db
from models.tasks import TaskUpdate
from models.cameras import CameraUpdate
from utils import parse_json
from pipeline import pipeline   # create base pipeline here

router = APIRouter()

@router.get("/tasks")
async def get_tasks():
    tasks = await db.tasks.find().to_list(length=100)
    return [parse_json(task) for task in tasks]

@router.post("/tasks")
async def create_task(manager_id: str, new_task: TaskUpdate):
    manager = await db.managers.find_one({"_id": ObjectId(manager_id)})
    if not manager:
        raise HTTPException(status_code=400, detail="Manager not found")

    threading.Thread(target=pipeline.run, args=(new_task.str_pipeline, )).start()

    new_task.manager_id = manager_id
    await db.managers.update_one({"_id": ObjectId(manager_id)}, {"$push": {"tasks": new_task.model_dump(by_alias=True)}})
    _task = await db.tasks.insert_one(new_task.model_dump(by_alias=True))

    for i, uri in enumerate(new_task.str_pipeline["source"]["properties"]["urls"]):
        new_camera = CameraUpdate(uri=uri, task_id=str(_task.inserted_id), is_active=True, source_id=i)
        _camera = await db.cameras.insert_one(new_camera.model_dump(by_alias=True))
        await db.tasks.update_one({"_id": ObjectId(new_camera.task_id)},{"$push": {"cameras": str(_camera.inserted_id)}})

    return {"message": "Task created successfully"}

@router.get("/tasks/{task_id}")
async def read_task(manager_id: str, task_id: str):
    manager = await db.managers.find_one({"_id": ObjectId(manager_id)})
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")
    
    task = await db.tasks.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return parse_json(task)

@router.put("/tasks/{task_id}")
async def update_task(manager_id: str, task_id : str, new_task: TaskUpdate):
    manager = await db.managers.find_one({"_id": ObjectId(manager_id)})
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")
    
    task = await db.tasks.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Release & run new pipeline
    pipeline.release_pipeline()
    threading.Thread(target=pipeline.run, args=(new_task.str_pipeline, )).start()

    # Update task in db
    await db.tasks.update_one({"_id" : ObjectId(task_id)}, {"$set": new_task.model_dump(by_alias=True, exclude_unset=True, exclude_defaults=True)})

    return {"message": "Task updated successfully"}

@router.delete("/tasks/{task_id}")
async def delete_task(manager_id: str, task_id: str):
    manager = await db.managers.find_one({"_id": ObjectId(manager_id)})
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")
    
    task = await db.tasks.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Stop pipeline
    pipeline.release_pipeline()

    # Delete task in db
    await db.tasks.delete_one({"_id": ObjectId(task_id)})

    return {"message": "Task deleted successfully"}
