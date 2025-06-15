import uuid
from datetime import datetime
from typing import List, Dict, Optional


class ConversationMemory:
    def __init__(self):
        self.conversations = {}

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self.conversations[session_id] = []
        return session_id

    def add_message(self, session_id: str, role: str, content: str):
        if session_id not in self.conversations:
            self.conversations[session_id] = []

        self.conversations[session_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

    def get_conversation_history(self, session_id: str, max_messages: Optional[int] = None) -> List[Dict]:
        if session_id not in self.conversations:
            return []

        history = self.conversations[session_id]
        if max_messages:
            history = history[-max_messages:]

        return history

    def format_history_for_prompt(self, session_id: str, max_messages: int = 5) -> str:
        history = self.get_conversation_history(session_id, max_messages)
        formatted_history = ""

        for msg in history:
            role = "Human" if msg["role"] == "user" else "Assistant"
            formatted_history += f"{role}: {msg['content']}\n\n"

        return formatted_history.strip()

    def clear_session(self, session_id: str):
        if session_id in self.conversations:
            self.conversations[session_id] = []

    def delete_session(self, session_id: str):
        if session_id in self.conversations:
            del self.conversations[session_id]

    def get_session_info(self, session_id: str) -> Dict:
        if session_id not in self.conversations:
            return {"error": "Session not found"}

        history = self.conversations[session_id]
        return {
            "session_id": session_id,
            "message_count": len(history),
            "created": history[0]["timestamp"] if history else None,
            "last_updated": history[-1]["timestamp"] if history else None
        }

    def list_sessions(self) -> List[str]:
        return list(self.conversations.keys())

    def get_session_summary(self, session_id: str, max_chars: int = 200) -> str:
        history = self.get_conversation_history(session_id)
        if not history:
            return "No conversation history"

        summary_parts = []
        char_count = 0

        for msg in history[:3]:
            role = "User" if msg["role"] == "user" else "Bot"
            content = msg["content"][:100] + \
                "..." if len(msg["content"]) > 100 else msg["content"]
            part = f"{role}: {content}"

            if char_count + len(part) > max_chars:
                break

            summary_parts.append(part)
            char_count += len(part)

        return " | ".join(summary_parts)
