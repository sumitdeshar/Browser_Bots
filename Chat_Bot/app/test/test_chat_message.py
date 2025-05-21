from app.utils.chatResponse import get_response  # ✅ correct

def test_get_response_hello():
    assert get_response("Hello") == "Hello there! How can I assist you?"

def test_get_response_how_are_you():
    assert get_response("How are you?") == "I'm doing well, thank you!  How about you?"

def test_get_response_goodbye():
    assert get_response("Goodbye") == "Goodbye! Have a great day."

def test_get_response_clear_chat():
    assert get_response("clear chat") is None

def test_get_response_unknown():
    assert get_response("Tell me a joke") == "I'm a very simple bot and I don't understand that yet.  Could you try rephrasing?"
