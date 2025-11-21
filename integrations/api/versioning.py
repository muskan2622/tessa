"""
API Versioning
Handle API versioning strategy
"""
from fastapi import APIRouter, Request
from fastapi.routing import APIRoute
from typing import Callable
import re


class VersionedAPIRouter(APIRouter):
    """API Router with versioning support"""
    
    def __init__(self, version: str = "v1", *args, **kwargs):
        """
        Initialize versioned router
        
        Args:
            version: API version (e.g., "v1", "v2")
        """
        prefix = kwargs.get("prefix", "") or ""
        if not prefix.startswith(f"/api/{version}"):
            kwargs["prefix"] = f"/api/{version}{prefix}"
        
        super().__init__(*args, **kwargs)
        self.version = version


def version_header_dependency(request: Request):
    """Extract API version from header"""
    version_header = request.headers.get("X-API-Version", "v1")
    # Validate version format
    if re.match(r"^v\d+$", version_header):
        return version_header
    return "v1"

