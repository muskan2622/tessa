"""
Webhook Events
Define webhook event types
"""
from enum import Enum


class WebhookEventType(str, Enum):
    """Webhook event types"""
    TITLE_SEARCH_STARTED = "title_search.started"
    TITLE_SEARCH_COMPLETED = "title_search.completed"
    TITLE_SEARCH_FAILED = "title_search.failed"
    DOCUMENT_UPLOADED = "document.uploaded"
    DOCUMENT_PROCESSED = "document.processed"
    RISK_SCORE_CALCULATED = "risk_score.calculated"
    COMPLIANCE_CHECK_COMPLETED = "compliance_check.completed"
    TITLE_ORDER_CREATED = "title_order.created"
    TITLE_ORDER_UPDATED = "title_order.updated"

