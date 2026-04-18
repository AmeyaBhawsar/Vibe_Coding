from fastapi import APIRouter, HTTPException, Header
from typing import List, Dict, Any
from app.schemas.payloads import TicketCreateRequest, TicketResponse, TicketReplyRequest
from app.services.ticket_service import TicketService
from app.data.mock_db import db
from datetime import datetime

router = APIRouter()

@router.get("/my", response_model=Dict[str, Any])
def get_my_tickets(user_id: str = Header(default="u1", alias="x-user-id")):
    try:
        tickets = TicketService.get_user_tickets(user_id)
        return {"tickets": tickets, "total_count": len(tickets)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=TicketResponse)
def create_new_ticket(payload: TicketCreateRequest, user_id: str = Header(default="u1", alias="x-user-id")):
    try:
        # Simulate passing the initial message as history
        history = [{"role": "user", "content": payload.subject}]
        ticket = TicketService.create_ticket(user_id, payload.category, history)
        return ticket
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary")
def get_my_summary(user_id: str = Header(default="u1", alias="x-user-id")):
    """Get counts for User Dash: open, inProgress, resolved"""
    user_tickets = [t for t in db["tickets"] if t["user_id"] == user_id]
    summary = {"open": 0, "inProgress": 0, "resolved": 0}
    for t in user_tickets:
        if t["status"] == "Open":
            summary["open"] += 1
        elif t["status"] == "In Progress":
            summary["inProgress"] += 1
        elif t["status"] == "Resolved":
            summary["resolved"] += 1
            
    return summary

@router.get("/{ticket_id}")
def get_ticket_details(ticket_id: str, user_id: str = Header(default="u1", alias="x-user-id")):
    """View specific ticket info for user"""
    ticket = next((t for t in db["tickets"] if t["id"] == ticket_id and t["user_id"] == user_id), None)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
        
    return {
        "ticket": ticket,
        "messages": [
            {"role": "user", "content": ticket["subject"], "timestamp": ticket["created_at"]}
        ]  # Mock message history
    }

@router.post("/{ticket_id}/reply")
def reply_to_ticket(ticket_id: str, payload: TicketReplyRequest, user_id: str = Header(default="u1", alias="x-user-id")):
    """User replies to an ongoing ticket"""
    ticket = next((t for t in db["tickets"] if t["id"] == ticket_id and t["user_id"] == user_id), None)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
        
    return {
        "messageId": f"msg-{int(datetime.now().timestamp())}",
        "timestamp": datetime.now().isoformat(),
        "success": True
    }