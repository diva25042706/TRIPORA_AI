from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException, status
from app.services.places_service import places_service
from app.schemas.place import PlaceSearchResponse, PlaceItem, CategoryCount, AreaZoneCount

router = APIRouter(prefix="/places", tags=["Places Discovery"])

@router.get("/search", response_model=PlaceSearchResponse)
async def search_places(
    query: Optional[str] = Query(None, description="Search query by name, locality, category, description"),
    category: Optional[str] = Query(None, description="Category filter (e.g. Beaches & Waterfronts)"),
    area_zone: Optional[str] = Query(None, description="Area zone: all, chennai_city, greater_chennai, day_trips"),
    sort_by: str = Query("default", description="Sort order: default, name_asc, name_desc, duration_asc, duration_desc, price_asc"),
    page: int = Query(1, ge=1, description="Page number, 1-indexed"),
    limit: int = Query(12, ge=1, le=100, description="Items per page")
):
    """
    Comprehensive destination discovery API returning verified places across Chennai metropolitan area
    and nearby day trips, supporting keyword search, multi-factor filtering, and pagination.
    """
    return places_service.search_places(
        query=query,
        category=category,
        area_zone=area_zone,
        sort_by=sort_by,
        page=page,
        limit=limit
    )

@router.get("/categories", response_model=List[CategoryCount])
async def get_categories():
    """Returns all available place categories with their item counts."""
    return places_service.get_categories()

@router.get("/zones", response_model=List[AreaZoneCount])
async def get_zones():
    """Returns area zone classifications (Chennai City, Greater Chennai Suburbs, Nearby Day Trips) with counts."""
    return places_service.get_zones()

@router.get("/{place_id}", response_model=PlaceItem)
async def get_place_detail(place_id: str):
    """Returns verified details for a single place."""
    place = places_service.get_place_by_id(place_id)
    if not place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Place with ID '{place_id}' not found in verified repository"
        )
    return place
