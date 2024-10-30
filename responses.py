import random
import chat

def handle_responses(message) -> str:
    p_message = message.lower()
    chat.get_response(p_message)
    return chat.get_response(p_message)
    