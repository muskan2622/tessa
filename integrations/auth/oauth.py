"""
OAuth 2.0 / OIDC Authentication
OAuth 2.0 and OpenID Connect integration
"""
from typing import Optional, Dict, Any
import aiohttp
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
import logging

logger = logging.getLogger(__name__)


class OAuthAuthenticator:
    """OAuth 2.0 / OIDC authentication handler"""
    
    def __init__(self, oauth_config: Dict[str, Any]):
        """
        Initialize OAuth authenticator
        
        Args:
            oauth_config: OAuth configuration dictionary
        """
        self.config = oauth_config
        self.oauth = OAuth(Config())
        
        # Register OAuth providers
        if oauth_config.get("google"):
            self.oauth.register(
                name="google",
                client_id=oauth_config["google"]["client_id"],
                client_secret=oauth_config["google"]["client_secret"],
                server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
                client_kwargs={"scope": "openid email profile"}
            )
        
        if oauth_config.get("azure_ad"):
            self.oauth.register(
                name="azure",
                client_id=oauth_config["azure_ad"]["client_id"],
                client_secret=oauth_config["azure_ad"]["client_secret"],
                server_metadata_url=f"https://login.microsoftonline.com/{oauth_config['azure_ad']['tenant_id']}/.well-known/openid-configuration",
                client_kwargs={"scope": "openid email profile"}
            )
        
        if oauth_config.get("okta"):
            okta_domain = oauth_config["okta"]["domain"]
            self.oauth.register(
                name="okta",
                client_id=oauth_config["okta"]["client_id"],
                client_secret=oauth_config["okta"]["client_secret"],
                server_metadata_url=f"https://{okta_domain}/.well-known/openid-configuration",
                client_kwargs={"scope": "openid email profile"}
            )
    
    async def get_authorization_url(
        self,
        provider: str,
        redirect_uri: str
    ) -> Optional[str]:
        """
        Get OAuth authorization URL
        
        Args:
            provider: OAuth provider name (google, azure, okta)
            redirect_uri: Redirect URI after authorization
            
        Returns:
            Authorization URL or None
        """
        try:
            client = self.oauth.create_client(provider)
            return await client.authorize_redirect(redirect_uri)
        except Exception as e:
            logger.error(f"Error generating OAuth authorization URL: {e}")
            return None
    
    async def process_callback(
        self,
        provider: str,
        request: Any,
        redirect_uri: str
    ) -> Optional[Dict[str, Any]]:
        """
        Process OAuth callback
        
        Args:
            provider: OAuth provider name
            request: FastAPI request object
            redirect_uri: Redirect URI
            
        Returns:
            User information dictionary or None
        """
        try:
            client = self.oauth.create_client(provider)
            token = await client.authorize_access_token(request)
            user_info = token.get("userinfo")
            
            if user_info:
                return {
                    "username": user_info.get("email") or user_info.get("sub"),
                    "email": user_info.get("email"),
                    "name": user_info.get("name"),
                    "provider": provider
                }
            return None
        except Exception as e:
            logger.error(f"Error processing OAuth callback: {e}")
            return None

