from sqlmodel import Session, select
# from app.models.chat import Message

# def get_response(user_message: str, db: Session) -> str:
#     """
#     Generates a basic chatbot response based on the user's message and optionally uses
#     the database session.
#     """
#     if "hello" in user_message.lower():
#         return "Hello there! How can I assist you?"
#     elif "how are you" in user_message.lower():
#         return "I'm doing well, thank you!  How about you?"
#     elif "goodbye" in user_message.lower() or "bye" in user_message.lower():
#         return "Goodbye! Have a great day."
#     elif "clear chat" in user_message.lower():
#         # Clear the chat history from the database
#         statement = select(Message)
#         results = db.exec(statement)
#         for message in results:
#             db.delete(message)
#         db.commit()
#         return "Chat history cleared from database."
#     else:
#         return "I'm a very simple bot and I don't understand that yet.  Could you try rephrasing?"
    
def get_response(user_message: str) -> str:
    """
    Generates a basic chatbot response based on the user's message and optionally uses
    the database session.
    """
    if "hello" in user_message.lower():
        return "Hello there! How can I assist you?"
    elif "how are you" in user_message.lower():
        return "I'm doing well, thank you!  How about you?"
    elif "goodbye" in user_message.lower() or "bye" in user_message.lower():
        return "Goodbye! Have a great day."
    elif "clear chat" in user_message.lower():
        return None
    else:
        return "I'm a very simple bot and I don't understand that yet.  Could you try rephrasing?"