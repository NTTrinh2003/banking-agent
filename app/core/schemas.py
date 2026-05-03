from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class Intent(str, Enum):
    TRANSFER_FAILURE = "transfer_failure"
    CARD_NOT_RECEIVED = "card_not_received"
    CARD_LOST = "card_lost"
    ACCOUNT_BLOCKED = "account_blocked"
    REFUND_REQUEST = "refund_request"
    BALANCE_INQUIRY = "balance_inquiry"
    SUSPICIOUS_TRANSACTION = "suspicious_transaction"
    GENERAL_INQUIRY = "general_inquiry"
    UNKNOWN = "unknown"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class RouterAction(str, Enum):
    SEND_REPLY = "send_reply"
    ASK_FOR_MORE_INFO = "ask_for_more_info"
    ESCALATE_TO_HUMAN = "escalate_to_human"

class IntentResult(BaseModel):
    """
    intent_node output
    """
    intent: Intent
    confidence: float = Field(ge=0.0, le=1.0)
    raw_label: Optional[str] = Field(
        default=None,
        description="Original label from Lab 2 model before mapping to Intent enum - useful for debugging label mismatches."
    )

class PriorityResult(BaseModel):
    """
    priority_node output
    """
    priority: Priority
    confidence: float = Field(ge=0.0, le=1.0)
    raw_label: Optional[str] = Field(
        description="Why this priority was assigned (e.g., 'matched keyword: blocked')."
    )

class PolicyResult(BaseModel):
    """
    policy_node output
    """
    policy_id: Optional[str] = None
    title: Optional[str] = None
    content: str = Field(
        description="Policy text passed to the draft node as grounding."
    )
    found: bool = Field(
        description="False when no policy matched the intent - draft node should handle gracefully."
    )

class DraftResult(BaseModel):
    draft_reply: str
    missing_information: list[str] = Field(
        default_factory=list,
        description="Fields the LLM thinks are needed (e.g., 'transaction date'). Populated via prompt instructions."
    )
    suggested_next_action: Optional[str] = None

class ValidationResult(BaseModel):
    action: RouterAction
    reason: str
    final_message: str = Field(
        description="E.g., 'draft too short', 'intent confidence below threshold', 'policy not found'."
    )

class RouterDecision(BaseModel):
    action: RouterAction
    reason: str
    final_message: str = Field(
        description="What to actually send: the draft, an info-request prompt, or an escalation notice."
    )

# API
class AgentTrace(BaseModel):
    intent: Optional[IntentResult] = None
    priority: Optional[PriorityResult] = None
    policy: Optional[PolicyResult] = None
    draft: Optional[DraftResult] = None
    validation: Optional[ValidationResult] = None
    router: Optional[RouterDecision] = None

class CustomerRequest(BaseModel):
    message: str = Field(
        min_length=1,
        description="Raw customer message in any language."
    )
    customer_id: Optional[str] = None

class FinalResponse(BaseModel):
    action: RouterAction
    message: str
    trace: AgentTrace