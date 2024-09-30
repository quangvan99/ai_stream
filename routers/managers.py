from fastapi import APIRouter, HTTPException
from bson import ObjectId

from database import db
from models.managers import ManagerUpdate
from utils import parse_json

router = APIRouter()

@router.get("/managers")
async def list_managers():
    managers = await db.managers.find().to_list(length=100)
    return [parse_json(manager) for manager in managers]

@router.post("/managers")
async def create_manager(manager: ManagerUpdate):
    existing_manager = await db.managers.find_one({"name": manager.name})
    if existing_manager:
        raise HTTPException(status_code=400, detail="Manager already exists")

    await db.managers.insert_one(manager.model_dump(by_alias=True))

    return {"message": "Manager created successfully"}

@router.get("/managers/{manager_id}")
async def read_manager(manager_id: str):
    manager = await db.managers.find_one({"_id": ObjectId(manager_id)})
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")
    
    return parse_json(manager)

@router.put("/managers/{manager_id}")
async def update_manager(manager_id: str, new_manager: ManagerUpdate):
    manager = await db.managers.find_one({"_id": ObjectId(manager_id)})
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")

    await db.managers.update_one({"_id": ObjectId(manager_id)}, {"$set": new_manager.model_dump(by_alias=True, exclude_unset=True, exclude_defaults=True)})

    return {"message": "Manager updated successfully"}

@router.delete("/managers/{manager_id}")
async def delete_manager(manager_id: str):
    manager = await db.managers.find_one({"_id": ObjectId(manager_id)})
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")

    await db.managers.delete_one({"_id": ObjectId(manager_id)})

    return {"message": "Manager deleted successfully"}
