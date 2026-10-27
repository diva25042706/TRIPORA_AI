from typing import List, Optional
from pydantic import BaseModel, Field

class PlaceItem(BaseModel):
    id: str
    name: str
    category: str
    area_zone: str = Field(description="chennai_city, greater_chennai, or day_trips")
    area_label: str
    locality: str
    city: str
    district: str
    address: str
    lat: float
    lng: float
    desc: str
    opening_hours: str
    closed_days: str
    ticket_price_inr: float = 0.0
    visit_duration_hours: float = 2.0
    is_outdoor: bool = True
    accessibility_notes: Optional[str] = None
    official_website: Optional[str] = None
    image_url: Optional[str] = None
    source_attribution: Optional[str] = "TTDC / Chennai Tourism"
    last_updated: Optional[str] = "2026-10-28"
    distance_km: Optional[float] = None
    travel_time_min: Optional[int] = None

class CategoryCount(BaseModel):
    category: str
    count: int

class AreaZoneCount(BaseModel):
    zone: str
    label: str
    count: int

class PlaceSearchResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    has_more: bool
    results: List[PlaceItem]
    available_categories: List[CategoryCount]
    available_zones: List[AreaZoneCount]
