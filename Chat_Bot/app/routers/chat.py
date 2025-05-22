# routes/user.py
from fastapi import APIRouter

from app.utils.chatResponse import ChatIntent, detect_intent, respond
from ..models.chat import Message

router = APIRouter(prefix="/message", tags=["Chat"])

# @router.get('/')
# async def find_all_users(db: AsyncIOMotorDatabase = Depends(get_database)):
#     users_cursor = db.user.find()
#     users = await users_cursor.to_list(length=100)
#     return serializeList(users)

# @router.get('/{id}')
# async def find_one_user(id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
#     user = await db.user.find_one({"_id": ObjectId(id)})
#     return serializeDict(user)

@router.post('/')
async def message_chatbot(user_input: Message):
    user_msg = user_input.message.lower()
    print(user_msg)
    intent = detect_intent(user_msg)
    reply = respond(intent, user_msg)
    return reply
    
