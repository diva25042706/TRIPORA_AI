from typing import List, Optional
from pydantic import BaseModel, Field

class PlaceItem(BaseModel):
    id: str
    name: str
    category: str
    subcategory: Optional[str] = None
    area_zone: Optional[str] = Field(default="district_attraction", description="chennai_city, greater_chennai, day_trips, or district_attraction")
    area_label: Optional[str] = None
    locality: str
    city: str
    district: str
    state: str = "Tamil Nadu"
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
    best_visiting_period: Optional[str] = None
    official_website: Optional[str] = None
    image_url: Optional[str] = None
    image_attribution: Optional[str] = "Tamil Nadu Tourism (TTDC)"
    source_attribution: Optional[str] = "TTDC / District Administration"
    source_confidence: Optional[str] = "verified_official"
    last_verified: Optional[str] = "2026-10-28"
    status: Optional[str] = "active"
    distance_km: Optional[float] = None
    travel_time_min: Optional[int] = None

class CategoryCount(BaseModel):
    category: str
    count: int

class AreaZoneCount(BaseModel):
    zone: str
    label: str
    count: int

class DistrictSummary(BaseModel):
    district: str
    district_key: str
    city: str
    lat: float
    lng: float
    attraction_count: int
    popular_attractions: List[str]

class PlaceSearchResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    has_more: bool
    results: List[PlaceItem]
    available_categories: List[CategoryCount]
    available_zones: List[AreaZoneCount]
    available_districts: Optional[List[DistrictSummary]] = None
