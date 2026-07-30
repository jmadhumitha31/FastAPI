# app/models.py

from dataclasses import dataclass


@dataclass
class Ticket:
    ticket_id: str
    customer_name: str
    priority: str
    status: str
    created_at: str
    resolved_at: str | None
    sla_breached: bool = False
    priority_score: int = 0