from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from datetime import datetime

# ─────────────────────────── Pydantic Models ───────────────────────────


class ChatMessage(BaseModel):
    role: str
    content: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_call_id: Optional[str] = None


class ChatRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    tools: Optional[List[Dict[str, Any]]] = None


class LogEntry(BaseModel):
    timestamp: datetime
    model: str
    tokens: int
    latency: int
    user_input: str
    response: str
    tool_used: Optional[List[str]] = None
    tool_input: Optional[List[str]] = None
    input_rejected: Optional[bool] = None  # True when validate_input raised
    output_fallback: Optional[bool] = None  # True when validate_out raised
    retry_count: Optional[int] = None  # Number of retries consumed


class CalculatorInput(BaseModel):
    expression: str


class ReadNotesInput(BaseModel):
    filename: str


class InputGuardrailError(Exception):
    pass


class OutputGuardrailError(Exception):
    pass
