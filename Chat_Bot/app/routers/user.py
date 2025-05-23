from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from app.schemas.user import UserResponseModel
from ..utils.hash import Hash
from ..models.user import User
from ..schemas.serializers import serializeDict, serializeList
from ..config.db import get_database, user_collection

router = APIRouter(prefix="/user", tags=["User"])


@router.get(
    '/',
    response_model=List[UserResponseModel],
    status_code=status.HTTP_200_OK,
    summary="Get all users",
    response_description="List of users"
)
async def find_all_users(db: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        users_cursor = user_collection.find()
        users = await users_cursor.to_list(length=100)
        return serializeList(users)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch users: {str(e)}"
        )


@router.get(
    '/{id}',
    response_model=UserResponseModel,
    status_code=status.HTTP_200_OK,
    summary="Get a user by ID",
    response_description="User data"
)
async def find_one_user(id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID")

        user = await user_collection.find_one({"_id": ObjectId(id)})
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return serializeDict(user)

    except HTTPException:
        raise  # re-raise known HTTP exceptions

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch user: {str(e)}"
        )


@router.post(
    '/create',
    response_model=List[UserResponseModel],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    response_description="List of all users after creation"
)
async def create_user(user_data: User, db: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        psd = user_data.password
        user_data.password = Hash.bcrypt(psd)

        await user_collection.insert_one(dict(user_data))

        users = await user_collection.find().to_list(length=100)
        print('user',users)
        return serializeList(users)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )


@router.put(
    '/update/{id}',
    response_model=UserResponseModel,
    status_code=status.HTTP_200_OK,
    summary="Update an existing user",
    response_description="Updated user data"
)
async def update_user(id: str, user_data: User, db: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID")

        update_result = await user_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": dict(user_data)},
            return_document=True  # return the updated document
        )
        if update_result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return serializeDict(update_result)

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user: {str(e)}"
        )


@router.delete(
    '/delete/{id}',
    response_model=UserResponseModel,
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    response_description="Deleted user data"
)
async def delete_user(id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    try:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID")

        deleted_user = await user_collection.find_one_and_delete({"_id": ObjectId(id)})
        if deleted_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return serializeDict(deleted_user)

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user: {str(e)}"
        )
