from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ItineraryItem(BaseModel):
    id: str
    day_number: int
    activity_name: str
    description: str
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    suggested_start_time: str
    estimated_duration_hours: float
    estimated_cost: float
    category: str = "Sightseeing"
    is_outdoor: bool = True
    data_source: str = "Curated Verified Catalog"
    relevant_notes: Optional[str] = None

class DayPlan(BaseModel):
    day_number: int
    date: str
    theme: str
    activities: List[ItineraryItem]
    day_cost: float
    day_notes: Optional[str] = None

class BudgetCategory(BaseModel):
    category: str
    amount: float
    percentage: float
    description: str
    is_estimate: bool = True

class BudgetBreakdown(BaseModel):
    total_budget: float
    total_estimated_cost: float
    remaining_budget: float
    budget_deficit: float
    budget_status: str  # "Under Budget", "Within Budget", "Over Budget"
    currency: str = "INR"
    cost_per_person: float
    categories: List[BudgetCategory]
    expensive_items: List[str]
    cost_saving_recommendations: List[str]
    calculation_notes: str

class TransportOption(BaseModel):
    id: str
    mode: str  # "Flight", "Train", "Bus", "Private Cab", "Self-Drive"
    origin: str
    destination: str
    distance_km: float
    duration_hours: float
    price_range_low: float
    price_range_high: float
    estimated_cost: float
    currency: str = "INR"
    is_recommended: bool = False
    recommendation_rationale: str
    source: str
    data_timestamp: str
    booking_advisory: str

    # Extended route validation and structured transit fields
    origin_coordinates: Optional[tuple[float, float]] = None
    destination_coordinates: Optional[tuple[float, float]] = None
    origin_station_or_airport: Optional[str] = None
    destination_station_or_airport: Optional[str] = None
    segments: List[Dict[str, Any]] = Field(default_factory=list)
    distance: float = 0.0
    distance_unit: str = "km"
    duration: float = 0.0
    departure_time: Optional[str] = None
    arrival_time: Optional[str] = None
    transfers: int = 0
    provider: str = "TRIPORA Verified Transit Engine"
    source_url: Optional[str] = None
    retrieved_at: str = ""
    data_status: str = "estimated"  # live_provider | verified_static | estimated | unavailable | demo_data
    verification_status: str = "estimated"  # verified | estimated | unverified
    recommendation_reason: str = ""
    warnings: List[str] = Field(default_factory=list)

class HotelOption(BaseModel):
    id: str
    name: str
    location: str
    price_per_night: float
    total_price: float
    currency: str = "INR"
    rating: Optional[float] = None
    amenities: List[str] = Field(default_factory=list)
    distance_to_center_km: float = 0.0
    description: str
    provider_source: str
    booking_url: Optional[str] = None
    is_verified: bool = True
    availability_status: str = "Available for inquiry"
    ranking_rationale: str

class WeatherForecast(BaseModel):
    date: str
    day_number: int
    condition: str
    temp_high_c: float
    temp_low_c: float
    precipitation_chance: int
    is_rainy: bool
    is_outdoor_suitable: bool
    risk_assessment: str
    suggested_alternatives: List[str] = Field(default_factory=list)
    affected_activities: List[str] = Field(default_factory=list)
    data_source: str
    freshness: str

class SafetyFinding(BaseModel):
    id: str
    title: str
    category: str  # "Official Advisory", "Reliability Check", "Weather Warning", "Schedule Conflict", "Health & Safety"
    severity: str  # "info", "low", "medium", "high"
    description: str
    supporting_source: str
    data_timestamp: str
    recommended_action: str
    confidence_notes: str

class AgentExecutionStatus(BaseModel):
    agent_name: str
    status: str  # "idle", "running", "completed", "failed", "skipped"
    duration_ms: int = 0
    summary: str
    error_message: Optional[str] = None

class FullTripPlan(BaseModel):
    trip_id: str
    title: str
    origin: str
    destination: str
    start_date: str
    end_date: str
    duration_days: int
    travellers: int
    total_budget: float
    currency: str = "INR"
    travel_style: str
    itinerary_explanation: str
    days: List[DayPlan]
    budget: BudgetBreakdown
    transports: List[TransportOption]
    hotels: List[HotelOption]
    weather_forecasts: List[WeatherForecast]
    safety_findings: List[SafetyFinding]
    agent_statuses: List[AgentExecutionStatus]
    data_source_metadata: Dict[str, Any] = Field(default_factory=dict)
    last_replanned_at: Optional[str] = None
