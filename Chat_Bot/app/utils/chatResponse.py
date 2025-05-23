from sqlmodel import Session, select
from enum import Enum
from datetime import datetime
import json

class ChatIntent(Enum):
    GREETING = "greeting"
    OPENING_HOURS = "opening hours"
    CLOSING_HOURS = "closing hours"
    SHOW_BOOKS = "show books"
    BOOK_PRICE = "book price"
    ORDER_BOOK = "order book"
    EXIT = "exit"
    HELP = "help"
    UNKNOWN = "unknown"

# bookstore = {
#     "opening_time": "9:00 AM",
#     "closing_time": "8:00 PM",
#     "books": {
#         "Python 101": 500,
#         "Learn AI": 700,
#         "Data Science Handbook": 850,
#         "Intro to Algorithms": 1000
#     }
# }
bookstore = {}

with open('app/utils/bookstore.json', 'r') as file:
    bookstore = json.load(file)


help_command ={
            "message": "Here are some things I can help you with:",
            "options": [
                {"id": 1, "command": "opening hours", "description": "Check the store's opening hours"},
                {"id": 2, "command": "closing hours", "description": "Check the store's closing hours"},
                {"id": 3, "command": "show books", "description": "View available books"},
                {"id": 4, "command": "book price", "description": "Find the price of a book"},
                {"id": 5, "command": "order book", "description": "Place an order for a book"},
                {"id": 6, "command": "exit", "description": "End the conversation"}
            ]
        }

def get_time_based_greeting() -> str:
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return "Good morning"
    elif 12 <= current_hour < 17:
        return "Good afternoon"
    elif 17 <= current_hour < 21:
        return "Good evening"
    else:
        return "Good night"

def detect_intent(user_input: str) -> ChatIntent:
    user_input = user_input.lower()

    greeting_keywords = ["hello", "hi", "namaste", "hey", "good morning", "good evening", "good afternoon"]
    
    if any(greet in user_input for greet in greeting_keywords):
        return ChatIntent.GREETING
    elif "open" in user_input:
        return ChatIntent.OPENING_HOURS
    elif "close" in user_input or "closing" in user_input:
        return ChatIntent.CLOSING_HOURS
    elif "show books" in user_input or "book list" in user_input:
        return ChatIntent.SHOW_BOOKS
    elif "price" in user_input:
        return ChatIntent.BOOK_PRICE
    elif "order" in user_input:
        return ChatIntent.ORDER_BOOK
    elif "bye" in user_input or "exit" in user_input:
        return ChatIntent.EXIT
    elif "help" in user_input:
        return ChatIntent.HELP
    else:
        return ChatIntent.UNKNOWN

def respond(intent: ChatIntent, user_input: str):
    if intent == ChatIntent.GREETING:
        time_greeting = get_time_based_greeting()
        return (
            f"{time_greeting}! Welcome to BookVerse Bookstore. 😊\n"
            "If you're not sure what to do, just type **help** and I’ll show you everything I can help with."
        )

    elif intent == ChatIntent.HELP:
        return help_command

    elif intent == ChatIntent.OPENING_HOURS:
        return f"We open at {bookstore['opening_time']}."

    elif intent == ChatIntent.CLOSING_HOURS:
        return f"We close at {bookstore['closing_time']}."

    elif intent == ChatIntent.SHOW_BOOKS:
        return "Here's our book list:\n" + "\n".join(f"- {book}" for book in bookstore['books'])

    elif intent == ChatIntent.BOOK_PRICE:
        for book in bookstore["books"]:
            if book.lower() in user_input.lower():
                return f"The price of '{book}' is Rs. {bookstore['books'][book]}"
        return "Please mention the book name to check the price."

    elif intent == ChatIntent.ORDER_BOOK:
        for book in bookstore["books"]:
            if book.lower() in user_input.lower():
                return f"Order placed for '{book}'. Total: Rs. {bookstore['books'][book]}. Thank you!"
        return "Sorry, we couldn't find the book. Please mention the correct book name."

    elif intent == ChatIntent.EXIT:
        return "Thank you for visiting our bookstore. Goodbye!"

    else:
        return "Sorry, I didn't understand that. You can type **help** to see what I can do."

