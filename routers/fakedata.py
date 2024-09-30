from fastapi import APIRouter
from database import db
from models.managers import ManagerUpdate
from models.tasks import TaskUpdate
from models.cameras import CameraUpdate

router = APIRouter()

@router.get("/gen_fake_data")
async def seed_data():
    await db["cameras"].delete_many({})
    await db["tasks"].delete_many({})
    await db["managers"].delete_many({})

    #-----------------------
    manager1 = ManagerUpdate(
        name="Task Manager 1",
        description="Description for Task Manager 1"
    )

    manager2 = ManagerUpdate(
        name="Task Manager 1",
        description="Description for Task Manager 2"
    )
    manager1 = await db.managers.insert_one(manager1.model_dump(by_alias=True))
    manager2 = await db.managers.insert_one(manager2.model_dump(by_alias=True))

    task1 = TaskUpdate(
        manager_id=str(manager1.inserted_id),
        name="Task 1",
        str_pipeline={"key": "value"}
    )
    task2 = TaskUpdate(
        manager_id=str(manager1.inserted_id),
        name="Task 2",
        str_pipeline={"key": "value"}
    )
    task3 = TaskUpdate(
        manager_id=str(manager2.inserted_id),
        name="Task 3",
        str_pipeline={"key": "value"}
    )
    task4 = TaskUpdate(
        manager_id=str(manager2.inserted_id),
        name="Task 4",
        str_pipeline={"key": "value"}
    )

    task1 = await db.tasks.insert_one(task1.model_dump(by_alias=True))
    task2 = await db.tasks.insert_one(task2.model_dump(by_alias=True))
    task3 = await db.tasks.insert_one(task3.model_dump(by_alias=True))
    task4 = await db.tasks.insert_one(task4.model_dump(by_alias=True))
    await db.managers.update_one({"_id": manager1.inserted_id}, {"$set": {"tasks": [str(task1.inserted_id), str(task2.inserted_id)]}})
    await db.managers.update_one({"_id": manager2.inserted_id}, {"$set": {"tasks": [str(task1.inserted_id), str(task2.inserted_id)]}})

    #-----------------------
    camera1 = CameraUpdate(
        uri="http://camera1",
        task_id=str(task1.inserted_id),
        info={'fps':30.0, 'width':1920, 'height':1080},
        source_id=0

    )

    camera2 = CameraUpdate(
        uri="http://camera2",
        task_id=str(task2.inserted_id),
        info={'fps':30.0, 'width':1920, 'height':1080},
        source_id=1
    )

    camera3 = CameraUpdate(
        uri="http://camera3",
        task_id=str(task3.inserted_id),
        info={'fps':30.0, 'width':1920, 'height':1080},
        source_id=0
    )

    camera4 = CameraUpdate(
        uri="http://camera4",
        task_id=str(task4.inserted_id),
        info={'fps':30.0, 'width':1920, 'height':1080},
        source_id=1
    )
    camera1_id = await db.cameras.insert_one(camera1.model_dump(by_alias=True))
    camera2_id = await db.cameras.insert_one(camera2.model_dump(by_alias=True))
    camera3_id = await db.cameras.insert_one(camera3.model_dump(by_alias=True))
    camera4_id = await db.cameras.insert_one(camera4.model_dump(by_alias=True))

    return {'mgs': "Data seeded successfully!"}