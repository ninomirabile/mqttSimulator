"""
Profile Routes - API endpoints for profile management.

This module provides FastAPI routes for listing available profiles,
getting profile information, and generating data previews.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from ..models import ProfileList, ProfileInfo, APIResponse
from ..services.mqtt_service import mqtt_service

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/", response_model=ProfileList)
async def list_profiles():
    """Get all available simulation profiles."""
    try:
        profiles = mqtt_service.get_available_profiles()
        return ProfileList(profiles=profiles)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting profiles: {str(e)}"
        )


@router.get("/{profile_name}", response_model=ProfileInfo)
async def get_profile_info(profile_name: str):
    """Get detailed information about a specific profile."""
    try:
        profile_info = mqtt_service.get_profile_info(profile_name)
        
        if profile_info is None:
            raise HTTPException(
                status_code=404,
                detail=f"Profile '{profile_name}' not found"
            )
        
        return profile_info
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting profile info: {str(e)}"
        )


@router.post("/{profile_name}/preview", response_model=APIResponse)
async def generate_profile_preview(profile_name: str, parameters: Dict[str, Any]):
    """Generate a preview of data for a profile with given parameters."""
    try:
        preview_data = mqtt_service.generate_profile_preview(profile_name, parameters)
        
        if preview_data is None:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to generate preview for profile '{profile_name}'"
            )
        
        return APIResponse(
            success=True,
            message=f"Preview generated for profile: {profile_name}",
            data={
                "profile": profile_name,
                "parameters": parameters,
                "preview": preview_data
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating preview: {str(e)}"
        ) 