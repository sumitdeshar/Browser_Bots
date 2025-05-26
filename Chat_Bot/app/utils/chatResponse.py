from sqlmodel import Session, select
from enum import Enum
from datetime import datetime
import json
import re

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
                {"id": 4, "command": "check price", "description": "Find the price of a book"},
                {"id": 5, "command": "order book", "description": "Place an order for a book"},
                {"id": 6, "command": "exit", "description": "End the conversation"}
            ]
        }

#more utlis
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

def show_books() -> str:
    books = bookstore["books"]
    return "📚 Here's our book list:\n" + "\n".join([f"- {book['name']}" for book in books])


def get_books(book_list: list) -> list:
    matched_books = []
    # Compile regex patterns for all user inputs (case-insensitive)
    patterns = [re.compile(re.escape(name), re.IGNORECASE) for name in book_list]

    for book in bookstore["books"]:
        for pattern in patterns:
            if pattern.search(book["name"]):
                matched_books.append(book)
                break  # Stop checking other patterns if matched

    return matched_books



def get_book_prices(book_list: list) -> str:
    matched = get_books(book_list)

    if matched:
        return "💰 Book Prices:\n" + "\n".join([f"{book['name']}: Rs. {book['price']}" for book in matched])
    else:
        return "❗ Please mention the correct book name to check the price."


def order_books(book_list: list) -> str:
    matched = get_books(book_list)

    if matched:
        total = sum(book["price"] for book in matched)
        order_details = "\n".join([f"🛒 Ordered: {book['name']} - Rs. {book['price']}" for book in matched])
        return f"{order_details}\n\n💸 Total: Rs. {total}\nWould you like to order more books?"
    else:
        return "❌ Sorry, we couldn't find any books in your order. Please try again."


def detect_intent(user_msg: dict) -> ChatIntent:
    user_input = user_msg['message'].lower()

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

def respond(intent: ChatIntent, user_input: dict):
    if intent == ChatIntent.GREETING:
        time_greeting = get_time_based_greeting()
        return (
            f"{time_greeting}! Welcome to BookVerse Bookstore. 😊\n"
            "If you're not sure what to do, just type **help** and I’ll show you everything I can help with."
        )

    elif intent == ChatIntent.HELP:
        return help_command

    elif intent == ChatIntent.OPENING_HOURS:
        return f"🕘 We open at {bookstore['opening_time']}."

    elif intent == ChatIntent.CLOSING_HOURS:
        return f"🕗 We close at {bookstore['closing_time']}."

    elif intent == ChatIntent.SHOW_BOOKS:
        return show_books()

    elif intent == ChatIntent.BOOK_PRICE:
        return get_book_prices(user_input['book_list'])

    elif intent == ChatIntent.ORDER_BOOK:
        return order_books(user_input['book_list'])

    elif intent == ChatIntent.EXIT:
        return "👋 Thank you for visiting our bookstore. Goodbye!"

    else:
        return "🤖 Sorry, I didn't understand that. You can type **help** to see what I can do."
