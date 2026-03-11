from pydantic import BaseModel, Field


class HarnessSettings(BaseModel):
    root_dir: str = Field(default="/home/netjer/.openclaw/workspace")
    violation_log: str = Field(default="./artifacts/violations.jsonl")
    audit_log: str = Field(default="./artifacts/audit.jsonl")
