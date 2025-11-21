"""
Salesforce Integration Client
Connects to Salesforce API for CRM integration
"""
import os
from typing import Dict, Any, List, Optional
from simple_salesforce import Salesforce
import logging

logger = logging.getLogger(__name__)


class SalesforceClient:
    """Salesforce API client"""
    
    def __init__(self):
        """Initialize Salesforce client"""
        self.username = os.getenv("SALESFORCE_USERNAME")
        self.password = os.getenv("SALESFORCE_PASSWORD")
        self.security_token = os.getenv("SALESFORCE_SECURITY_TOKEN")
        self.domain = os.getenv("SALESFORCE_DOMAIN", "login")
        
        if self.username and self.password:
            try:
                self.sf = Salesforce(
                    username=self.username,
                    password=self.password,
                    security_token=self.security_token,
                    domain=self.domain
                )
                self.connected = True
            except Exception as e:
                logger.error(f"Failed to connect to Salesforce: {e}")
                self.connected = False
        else:
            self.connected = False
            logger.warning("Salesforce credentials not configured")
    
    def create_title_order(
        self,
        property_address: Dict[str, str],
        contact_id: str,
        opportunity_id: str = None
    ) -> Optional[str]:
        """
        Create a Title Order custom object in Salesforce
        
        Args:
            property_address: Property address dictionary
            contact_id: Salesforce Contact ID
            opportunity_id: Salesforce Opportunity ID (optional)
            
        Returns:
            Salesforce record ID or None
        """
        if not self.connected:
            logger.error("Salesforce not connected")
            return None
        
        try:
            # Create Title Order record
            title_order_data = {
                "Property_Address__c": f"{property_address.get('street')}, {property_address.get('city')}, {property_address.get('state')} {property_address.get('zip_code')}",
                "Contact__c": contact_id,
                "Status__c": "New"
            }
            
            if opportunity_id:
                title_order_data["Opportunity__c"] = opportunity_id
            
            result = self.sf.Title_Order__c.create(title_order_data)
            return result.get("id")
        except Exception as e:
            logger.error(f"Error creating Title Order in Salesforce: {e}")
            return None
    
    def update_title_search_result(
        self,
        title_order_id: str,
        search_result: Dict[str, Any]
    ) -> bool:
        """
        Update Title Order with search results
        
        Args:
            title_order_id: Salesforce Title Order ID
            search_result: Title search result dictionary
            
        Returns:
            True if successful, False otherwise
        """
        if not self.connected:
            return False
        
        try:
            update_data = {
                "Search_Status__c": search_result.get("status"),
                "Risk_Score__c": search_result.get("risk_score"),
                "Number_of_Liens__c": len(search_result.get("liens", [])),
                "Number_of_Encumbrances__c": len(search_result.get("encumbrances", []))
            }
            
            self.sf.Title_Order__c.update(title_order_id, update_data)
            return True
        except Exception as e:
            logger.error(f"Error updating Title Order in Salesforce: {e}")
            return False
    
    def create_workflow_task(
        self,
        title_order_id: str,
        task_subject: str,
        task_description: str
    ) -> Optional[str]:
        """
        Create a workflow task in Salesforce
        
        Args:
            title_order_id: Salesforce Title Order ID
            task_subject: Task subject
            task_description: Task description
            
        Returns:
            Task ID or None
        """
        if not self.connected:
            return None
        
        try:
            task_data = {
                "WhatId": title_order_id,
                "Subject": task_subject,
                "Description": task_description,
                "Status": "Not Started",
                "Priority": "Normal"
            }
            
            result = self.sf.Task.create(task_data)
            return result.get("id")
        except Exception as e:
            logger.error(f"Error creating task in Salesforce: {e}")
            return None

