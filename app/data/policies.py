"""
Dummy policy

Can be Postgres, online query,...
"""

from app.core.schemas import Intent, PolicyResult

_POLICIES: dict[Intent, dict[str, str]] = {
    Intent.TRANSFER_FAILURE: {
        "policy_id": "POL-001",
        "title": "Failed Transfer Handling",
        "content":  (
            "If a transfer fails, the amount is automatically returned to the sender's "
            "account within 1-3 business days. Customers should provide the transaction "
            "reference number, transfer date, and recipient account details. "
            "If the amount has been debited but not refunded after 3 business days, "
            "the case must be escalated to the operations team."
        )
    },

    Intent.CARD_NOT_RECEIVED: {
        "policy_id": "POL-002",
        "title": "Card Delivery Issues",
        "content": (
            "Standard card delivery takes 7-10 business days from issuance. "
            "If the card has not arrived after 10 business days, customers should "
            "verify their registered mailing address and request a replacement. "
            "A replacement card is issued free of charge for the first occurrence."
        )
    },

    Intent.CARD_LOST: {
        "policy_id": "POL-003",
        "title": "Lost or Stolen Card",
        "content": (
            "Lost or stolen cards must be blocked immediately to prevent unauthorized use. "
            "Customers can block a card via the mobile app, internet banking, or by "
            "calling the 24/7 hotline. A replacement card will be issued within 5-7 "
            "business days. Any unauthorized transactions before blocking should be "
            "reported within 60 days for dispute review."
        )
    },

    Intent.ACCOUNT_BLOCKED: {
        "policy_id": "POL-004",
        "title": "Account Block Resolution",
        "content": (
            "Accounts may be blocked due to suspicious activity, multiple failed login "
            "attempts, or compliance review. To unblock, customers must verify their "
            "identity via the mobile app or by visiting a branch with a valid ID. "
            "Compliance-related blocks require additional review and must be escalated "
            "to the risk team."
        ),
    },

    Intent.REFUND_REQUEST: {
        "policy_id": "POL-005",
        "title": "Refund Request Processing",
        "content": (
            "Refund requests for disputed transactions must be submitted within 60 days "
            "of the transaction date. Required information: transaction ID, date, amount, "
            "and reason for dispute. Standard processing time is 7-14 business days. "
            "Refunds for merchant-related disputes may take up to 45 days pending "
            "merchant response."
        ),
    },

    Intent.BALANCE_INQUIRY: {
        "policy_id": "POL-006",
        "title": "Balance and Account Information",
        "content": (
            "Customers can check their balance via the mobile app, internet banking, "
            "ATM, or by calling the automated hotline. For security reasons, account "
            "balance details are not disclosed over chat or email and require "
            "authenticated channels."
        ),
    },

    Intent.SUSPICIOUS_TRANSACTION: {
        "policy_id": "POL-007",
        "title": "Suspicious Transaction Reporting",
        "content": (
            "Any transaction the customer does not recognize must be reported immediately. "
            "The card or account will be temporarily frozen pending investigation. "
            "Customers should provide the transaction date, amount, and merchant name. "
            "All suspicious transaction cases are high priority and require human review."
        ),
    },

    Intent.GENERAL_INQUIRY: {
        "policy_id": "POL-008",
        "title": "General Customer Support",
        "content": (
            "For general questions about products, fees, or services, customers can "
            "consult the help center or contact support via chat, phone, or email. "
            "Support hours are 24/7 for card and security issues, and 8AM-10PM for "
            "general inquiries."
        ),
    },
}

def get_policy(intent: Intent) -> PolicyResult:
    """ Look up the policy for a given intent """
    entry = _POLICIES.get(intent)

    if entry is None:
        # No raise -> Keep robust workflow
        return PolicyResult(
            policy_id=None,
            title=None,
            content="No specify policy fount for this intent. Escalation recommended.",
            found=False, # To escalate
        )

    return PolicyResult(
        policy_id=entry["policy_id"],
        title=entry["title"],
        content=entry["content"],
        found=True,
    )

def list_available_intents() -> list[Intent]:
    """ Returns defined policies """
    return list(_POLICIES.keys())