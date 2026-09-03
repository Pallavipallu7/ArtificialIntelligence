from backend.agent.dialogue_manager import process_chat_dialogue
from backend.reasoning.kb import KnowledgeBase

def handle_chatbot_message(message: str, session_id: str = "default", kb: KnowledgeBase = None):
    return process_chat_dialogue(message, session_id=session_id, kb=kb)
