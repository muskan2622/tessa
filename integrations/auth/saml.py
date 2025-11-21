"""
SAML 2.0 Authentication
SAML SSO integration
"""
from typing import Optional, Dict, Any
import os
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils
import logging

logger = logging.getLogger(__name__)


class SAMLAuthenticator:
    """SAML 2.0 authentication handler"""
    
    def __init__(self, saml_config: Dict[str, Any]):
        """
        Initialize SAML authenticator
        
        Args:
            saml_config: SAML configuration dictionary
        """
        self.config = saml_config
        self.settings = {
            "sp": {
                "entityId": saml_config.get("sp_entity_id"),
                "assertionConsumerService": {
                    "url": saml_config.get("acs_url"),
                    "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
                },
                "singleLogoutService": {
                    "url": saml_config.get("slo_url"),
                    "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
                },
                "x509cert": saml_config.get("sp_certificate"),
                "privateKey": saml_config.get("sp_private_key")
            },
            "idp": {
                "entityId": saml_config.get("idp_entity_id"),
                "singleSignOnService": {
                    "url": saml_config.get("idp_sso_url"),
                    "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
                },
                "x509cert": saml_config.get("idp_certificate")
            }
        }
    
    def prepare_request(self, request_data: Dict[str, Any]) -> OneLogin_Saml2_Auth:
        """
        Prepare SAML request
        
        Args:
            request_data: Request data dictionary
            
        Returns:
            SAML Auth object
        """
        return OneLogin_Saml2_Auth(request_data, self.settings)
    
    def get_login_url(self, request_data: Dict[str, Any]) -> Optional[str]:
        """
        Get SAML login URL
        
        Args:
            request_data: Request data dictionary
            
        Returns:
            Login URL or None
        """
        try:
            auth = self.prepare_request(request_data)
            return auth.login()
        except Exception as e:
            logger.error(f"Error generating SAML login URL: {e}")
            return None
    
    def process_response(
        self,
        request_data: Dict[str, Any],
        saml_response: str
    ) -> Optional[Dict[str, Any]]:
        """
        Process SAML response
        
        Args:
            request_data: Request data dictionary
            saml_response: SAML response string
            
        Returns:
            User attributes dictionary or None
        """
        try:
            auth = self.prepare_request(request_data)
            auth.process_response(saml_response)
            
            if auth.is_authenticated():
                attributes = auth.get_attributes()
                return {
                    "username": attributes.get("username", [None])[0],
                    "email": attributes.get("email", [None])[0],
                    "name": attributes.get("name", [None])[0],
                    "saml_session_index": auth.get_session_index()
                }
            else:
                logger.warning("SAML authentication failed")
                return None
        except Exception as e:
            logger.error(f"Error processing SAML response: {e}")
            return None

