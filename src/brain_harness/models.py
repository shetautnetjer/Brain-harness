from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class ViolationRecord(BaseModel):
    event_type: Literal[
        "taxonomy_violation",
        "provenance_violation",
        "plane_separation_violation",
        "source_events_gate_failure",
    ]
    severity: Literal["warning", "error"]
    message: str
    context: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class RetrievalResult(BaseModel):
    intent: str
    query_plan: list[str]
    records: list[dict[str, Any]] = Field(default_factory=list)
    citations: list[str] = Field(default_factory=list)
    used_vector_search: bool = False
    escalated_to_plane_b: bool = False
    warnings: list[str] = Field(default_factory=list)
