# routes/user.py
from fastapi import APIRouter, Depends
from ..models.user import User 
from ..schemas.user import serializeDict, serializeList
from bson import ObjectId
from ..config.db import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(prefix="/user", tags=["User"])

@router.get('/')
async def find_all_users(db: AsyncIOMotorDatabase = Depends(get_database)):
    users_cursor = db.user.find()
    users = await users_cursor.to_list(length=100)
    return serializeList(users)

@router.get('/{id}')
async def find_one_user(id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    user = await db.user.find_one({"_id": ObjectId(id)})
    return serializeDict(user)

@router.post('/')
async def create_user(user_data: User, db: AsyncIOMotorDatabase = Depends(get_database)):
    await db.user.insert_one(dict(user_data))
    users = await db.user.find().to_list(length=100)
    return serializeList(users)

@router.put('/{id}')
async def update_user(id: str, user_data: User, db: AsyncIOMotorDatabase = Depends(get_database)):
    await db.user.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": dict(user_data)}
    )
    updated_user = await db.user.find_one({"_id": ObjectId(id)})
    return serializeDict(updated_user)

@router.delete('/{id}')
async def delete_user(id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    deleted_user = await db.user.find_one_and_delete({"_id": ObjectId(id)})
    return serializeDict(deleted_user)
