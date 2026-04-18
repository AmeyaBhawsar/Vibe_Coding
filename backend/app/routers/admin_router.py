from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from app.data.mock_db import db
from app.schemas.payloads import (
    AdminBulkUpdateRequest, AdminUpdateTicketRequest, AdminNoteRequest,
    UpdateAutomationsRequest, TestAutoRuleRequest, ExecuteRunbookRequest,
    InviteUserRequest, UpdatePermissionsRequest, CreateKBEntryRequest
)
from datetime import datetime
import uuid
from app.data.mock_db import db

router = APIRouter()

# --- ADMIN TICKET APIs ---
@router.get("/tickets")
def get_all_tickets():
    """Fetch all tickets for the Admin Queue"""
    return {"tickets": db["tickets"], "total_count": len(db["tickets"])}

@router.get("/tickets/{ticket_id}")
def get_ticket_details(ticket_id: str):
    """Get full details for a specific ticket"""
    ticket = next((t for t in db["tickets"] if t["id"] == ticket_id), None)
    return ticket or {"error": "Ticket not found"}

@router.patch("/tickets/bulk")
def bulk_update_tickets(payload: AdminBulkUpdateRequest):
    count = 0
    for t in db["tickets"]:
        if t["id"] in payload.ticket_ids:
            t[payload.action] = payload.value
            count += 1
    return {"success": True, "updatedCount": count}

@router.patch("/tickets/{ticket_id}")
def update_ticket_properties(ticket_id: str, payload: AdminUpdateTicketRequest):
    """Update ticket properties (e.g., status, assignee, priority)"""
    for t in db["tickets"]:
        if t["id"] == ticket_id:
            if payload.status:
                t["status"] = payload.status
            if payload.assignee_id:
                t["assignee_id"] = payload.assignee_id
            if payload.priority:
                t["priority"] = payload.priority
            return {"success": True, "updatedTicket": t}
    raise HTTPException(status_code=404, detail="Ticket not found")

@router.post("/tickets/{ticket_id}/notes")
def add_admin_note(ticket_id: str, payload: AdminNoteRequest):
    """Add reply or internal note"""
    return {
        "messageId": f"note-{int(datetime.now().timestamp())}",
        "timestamp": datetime.now().isoformat(),
        "isInternalNote": payload.is_internal_note,
        "success": True
    }

# --- ADMIN ANALYTICS APIs ---
@router.get("/metrics")
def get_dashboard_metrics():
    """Data for the top KPI cards on Admin Dashboard"""
    total = len(db["tickets"])
    resolved = len([t for t in db["tickets"] if t["status"] == "Resolved"])
    open_tickets = total - resolved
    return {
        "active_backlog": open_tickets,
        "resolved_by_it": resolved,
        "auto_resolved_bot": 1432, # Mock data based on your UI image
        "avg_resolution_time": "2h 15m"
    }

@router.get("/metrics/trends")
def get_resolution_trends(timeframe: str = "7d"):
    """Data for the line chart"""
    return {
        "chartData": [
            {"date": "2023-10-01", "value": 45},
            {"date": "2023-10-02", "value": 52},
            {"date": "2023-10-03", "value": 38}
        ]
    }

@router.get("/metrics/severity")
def get_severity_distribution():
    """Data for the donut chart"""
    return {
        "pieData": [
            {"id": "P1", "label": "P1 - Critical", "value": 10},
            {"id": "P2", "label": "P2 - High", "value": 25},
            {"id": "P3", "label": "P3 - Medium", "value": 40},
            {"id": "P4", "label": "P4 - Low", "value": 25}
        ]
    }

@router.get("/metrics/backlog")
def get_backlog_breakdown():
    """Data for backlog table"""
    return {
        "statusCounts": {"Open": 15, "In Progress": 8, "On Hold": 3},
        "avgAge": "3.5 days"
    }

# --- ADMIN USERS & ROLES APIs ---
@router.get("/users")
def get_all_users():
    """List all users for Role Management"""
    return {"users": db["users"]}

@router.patch("/users/{user_id}/role")
def update_user_role(user_id: str, new_role: str):
    """Promote or demote a user"""
    for u in db["users"]:
        if u["id"] == user_id:
            u["role"] = new_role
            return {"success": True, "user": u}
    return {"error": "User not found"}

@router.post("/users/invite")
def invite_user(payload: InviteUserRequest):
    """Send email invite to platform"""
    new_user = {
        "id": f"u-{str(uuid.uuid4())[:8]}",
        "name": "Invited User",
        "email": payload.email,
        "role": payload.assigned_role
    }
    db["users"].append(new_user)
    return {"success": True, "message": f"Invite sent to {payload.email}"}

@router.get("/roles/matrix")
def get_permissions_matrix():
    """Fetch permission matrix checkboxes"""
    return {
        "roles": ["Admin", "Technician", "User"],
        "permissions": ["manage_users", "view_reports", "edit_kb", "resolve_tickets"]
    }

@router.put("/roles/matrix")
def update_permissions_matrix(payload: UpdatePermissionsRequest):
    """Save changes to global roles"""
    return {"success": True, "message": "Permissions updated successfully"}

@router.get("/audit-logs")
def get_activity_log(page: int = 1, limit: int = 10):
    """Fetch system user changes"""
    return {
        "logs": [
            {
                "id": f"log-{str(uuid.uuid4())[:8]}", 
                "action": "User Promoted", 
                "actor": "Admin System", 
                "target": "David Kim", 
                "date": datetime.now().isoformat()
            }
        ],
        "total": 1
    }

# --- ADMIN KNOWLEDGE BASE & AUTOMATION APIs ---
@router.get("/kb")
def get_knowledge_base():
    """View all KB articles and Runbooks"""
    return {"kb_entries": db["kb"]}

@router.get("/automations")
def get_automation_rules():
    """Fetch AI confidence thresholds and intent maps"""
    return {
        "confidence_thresholds": {"auto_resolve": 90, "category_assign": 75},
        "approval_gates": ["Database Restarts", "Access Provisioning"]
    }

@router.put("/automations")
def update_automation_rules(payload: UpdateAutomationsRequest):
    """Save rule builder configuration"""
    return {"success": True, "updatedRules": payload.rules_data}

@router.post("/automations/test")
def test_ai_rule(payload: TestAutoRuleRequest):
    """Test console for prompts"""
    return {
        "simulatedIntent": "password_reset",
        "confidence": 0.95
    }

@router.post("/runbooks/exec")
def execute_runbook(payload: ExecuteRunbookRequest):
    """Trigger quick action"""
    return {
        "executionStatus": "completed",
        "logs": [f"Executed runbook {payload.runbook_id} for ticket {payload.ticket_id}"]
    }

@router.post("/kb")
def add_update_kb_entry(payload: CreateKBEntryRequest):
    """Save new solution/runbook"""
    new_entry = {
         "id": f"kb-{str(uuid.uuid4())[:8]}",
         "category": "Custom",
         "keywords": payload.tags or [],
         "resolution_steps": payload.content
    }
    db["kb"].append(new_entry)
    return {"articleId": new_entry["id"], "success": True}