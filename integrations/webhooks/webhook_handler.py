"""
Webhook Handler
Handles webhook delivery and retries
"""
import asyncio
import aiohttp
import hmac
import hashlib
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class WebhookHandler:
    """Handle webhook deliveries"""
    
    def __init__(self):
        """Initialize webhook handler"""
        self.max_retries = 3
        self.retry_delays = [1, 5, 15]  # seconds
    
    def generate_signature(
        self,
        payload: str,
        secret: str
    ) -> str:
        """
        Generate webhook signature
        
        Args:
            payload: Webhook payload as string
            secret: Webhook secret
            
        Returns:
            HMAC signature
        """
        return hmac.new(
            secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    async def deliver_webhook(
        self,
        url: str,
        event_type: str,
        payload: Dict[str, Any],
        secret: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Deliver webhook to URL
        
        Args:
            url: Webhook URL
            event_type: Event type
            payload: Payload dictionary
            secret: Optional webhook secret for signing
            
        Returns:
            Delivery result dictionary
        """
        payload_json = json.dumps(payload)
        headers = {
            "Content-Type": "application/json",
            "X-Webhook-Event": event_type,
            "X-Webhook-Timestamp": datetime.utcnow().isoformat()
        }
        
        # Add signature if secret provided
        if secret:
            signature = self.generate_signature(payload_json, secret)
            headers["X-Webhook-Signature"] = f"sha256={signature}"
        
        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        url,
                        data=payload_json,
                        headers=headers,
                        timeout=aiohttp.ClientTimeout(total=30)
                    ) as response:
                        if response.status >= 200 and response.status < 300:
                            return {
                                "success": True,
                                "status_code": response.status,
                                "attempt": attempt + 1
                            }
                        else:
                            error_text = await response.text()
                            logger.warning(
                                f"Webhook delivery failed: {response.status} - {error_text}"
                            )
            except Exception as e:
                logger.error(f"Webhook delivery error (attempt {attempt + 1}): {e}")
            
            # Wait before retry (except on last attempt)
            if attempt < self.max_retries - 1:
                await asyncio.sleep(self.retry_delays[attempt])
        
        return {
            "success": False,
            "status_code": None,
            "attempt": self.max_retries
        }
    
    async def deliver_to_all_webhooks(
        self,
        webhooks: List[Dict[str, Any]],
        event_type: str,
        payload: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Deliver webhook to multiple endpoints
        
        Args:
            webhooks: List of webhook configurations
            event_type: Event type
            payload: Payload dictionary
            
        Returns:
            List of delivery results
        """
        tasks = []
        for webhook in webhooks:
            if event_type in webhook.get("event_types", []):
                task = self.deliver_webhook(
                    url=webhook["url"],
                    event_type=event_type,
                    payload=payload,
                    secret=webhook.get("secret")
                )
                tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

