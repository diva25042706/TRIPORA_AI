from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator
from app.schemas.agent_schemas import FullTripPlan

class TripCreateRequest(BaseModel):
    title: Optional[str] = None
    origin: str = Field(..., min_length=2, description="Departure location / city")
    destination: str = Field(..., min_length=2, description="Target travel destination")
    start_date: str = Field(..., description="Start date in YYYY-MM-DD format")
    end_date: str = Field(..., description="End date in YYYY-MM-DD format")
    travellers: int = Field(default=1, ge=1, le=50, description="Number of travellers")
    total_budget: float = Field(..., gt=0, description="Total budget in specified currency")
    currency: str = Field(default="INR", description="Default INR or currency code")
    travel_style: str = Field(default="Balanced", description="Budget, Balanced, Luxury, Adventurous, Relaxed")
    interests: List[str] = Field(default_factory=lambda: ["Culture", "Food", "Sightseeing"])
    accommodation_pref: str = Field(default="Hotel", description="Hostel, Hotel, Resort, Boutique, Apartment")
    transport_pref: str = Field(default="Best Value", description="Flight, Train, Bus, Self-Drive, Best Value")

    @field_validator("end_date")
    @classmethod
    def validate_dates(cls, v, values):
        # We can validate format and order
        return v

class TripUpdateRequest(BaseModel):
    title: Optional[str] = None
    total_budget: Optional[float] = None
    travel_style: Optional[str] = None
    interests: Optional[List[str]] = None
    accommodation_pref: Optional[str] = None
    transport_pref: Optional[str] = None

class ReplanRequest(BaseModel):
    instruction: str = Field(..., description="e.g. 'Reduce budget by 20%', 'Rain on Day 2 - swap outdoor activities', 'Make pace more relaxed'")
    specific_day: Optional[int] = Field(None, description="Optional single day to replan")
    new_budget: Optional[float] = Field(None, description="Optional revised budget")
    new_interests: Optional[List[str]] = Field(None, description="Optional updated interests")
    new_travel_style: Optional[str] = Field(None, description="Optional updated travel style")
    new_transport_pref: Optional[str] = Field(None, description="Optional updated transport preference")
    new_accommodation_pref: Optional[str] = Field(None, description="Optional updated accommodation preference")

class ReplanDiffSummary(BaseModel):
    cost_difference: float
    previous_total: float
    new_total: float
    currency: str
    changes_summary: List[str]
    affected_days: List[int]
    notes: str

class ReplanResponse(BaseModel):
    trip_id: str
    diff_summary: ReplanDiffSummary
    updated_plan: FullTripPlan

class TripResponse(BaseModel):
    id: str
    user_id: int
    title: str
    origin: str
    destination: str
    start_date: str
    end_date: str
    duration_days: int
    travellers: int
    total_budget: float
    currency: str
    travel_style: str
    interests: List[str]
    accommodation_pref: str
    transport_pref: str
    status: str
    full_trip_data: Optional[FullTripPlan] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TripSummary(BaseModel):
    id: str
    title: str
    origin: str
    destination: str
    start_date: str
    end_date: str
    duration_days: int
    travellers: int
    total_budget: float
    currency: str
    travel_style: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
