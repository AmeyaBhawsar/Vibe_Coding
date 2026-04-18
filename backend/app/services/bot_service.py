import uuid
from app.data.mock_db import db
from app.services.kb_service import KnowledgeBaseService
from app.services.ticket_service import TicketService

class BotService:
    @staticmethod
    def process_message(user_id: str, chat_id: str | None, message: str) -> dict:
        # Initialize chat session if new
        if not chat_id or chat_id not in db["chats"]:
            chat_id = chat_id or str(uuid.uuid4())
            db["chats"][chat_id] = {"history": [], "failed_attempts": 0}

        session = db["chats"][chat_id]
        session["history"].append({"role": "user", "content": message})

        reply = ""
        requires_confirmation = False

        # Check for User Feedback (Yes/No)
        user_text = message.lower().strip()
        is_no = user_text == 'no'
        is_yes = user_text == 'yes'

        if is_yes:
            reply = "Great! I'm glad I could help. Closing this chat."
            session["failed_attempts"] = 0
            
        elif is_no:
            session["failed_attempts"] += 1
            
            # ESCALATION PROTOCOL: 2 Failed Attempts
            if session["failed_attempts"] >= 2:
                ticket = TicketService.create_ticket(user_id, 'Escalated', session["history"])
                reply = f"I apologize, but I am unable to resolve this. I have escalated this to our human IT team. Your ticket ID is **{ticket['id']}**."
            else:
                reply = "I'm sorry that didn't work. Could you provide a bit more detail about the error?"
                
        else:
            # Normal KB Search Flow
            solution = KnowledgeBaseService.search(message)
            if solution:
                reply = f"{solution}\n\nDid this resolve your issue? (Yes/No)"
                requires_confirmation = True
            else:
                reply = "I couldn't find a direct fix for that. Could you try rephrasing your issue?"

        session["history"].append({"role": "bot", "content": reply})

        return {
            "chat_id": chat_id,
            "reply": reply,
            "requires_confirmation": requires_confirmation,
            "failed_attempts": session["failed_attempts"]
        }