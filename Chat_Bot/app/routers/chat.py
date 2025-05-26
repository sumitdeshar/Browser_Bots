# routes/user.py
from fastapi import APIRouter

from app.utils.chatResponse import detect_intent, respond
from ..schemas.chat import Message

router = APIRouter(prefix="/message", tags=["Chat"])

@router.post('/')
async def message_chatbot(user_input: Message):
    user_msg = {}
    user_msg['message'] = user_input.message
    user_msg['book_list'] = user_input.book_list
    print(user_msg)
    intent = detect_intent(user_msg)
    reply = respond(intent, user_msg)
    return reply
    
