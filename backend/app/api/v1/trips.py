from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.trip import (
    TripCreateRequest,
    TripUpdateRequest,
    TripResponse,
    TripSummary,
    ReplanRequest,
    ReplanResponse
)
from app.services.trip_service import trip_service

router = APIRouter(prefix="/trips", tags=["Trips"])

@router.post("/", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
async def create_trip(
    req: TripCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Trigger the multi-agent LangGraph orchestration to plan and persist a new trip."""
    trip = await trip_service.create_and_plan_trip(db, current_user, req)
    return TripResponse.model_validate(trip)

@router.get("/", response_model=List[TripSummary])
def list_trips(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve all trips owned by the current user."""
    trips = trip_service.list_user_trips(db, current_user.id)
    return [TripSummary.model_validate(t) for t in trips]

@router.get("/{trip_id}", response_model=TripResponse)
def get_trip(
    trip_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve a single trip by ID with ownership enforcement."""
    trip = trip_service.get_trip_by_id(db, trip_id, current_user.id)
    return TripResponse.model_validate(trip)

@router.put("/{trip_id}", response_model=TripResponse)
def update_trip(
    trip_id: str,
    req: TripUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update trip properties or preferences."""
    trip = trip_service.update_trip(db, trip_id, current_user.id, req)
    return TripResponse.model_validate(trip)

@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trip(
    trip_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a saved trip."""
    trip_service.delete_trip(db, trip_id, current_user.id)
    return None

@router.post("/{trip_id}/replan", response_model=ReplanResponse)
async def replan_trip(
    trip_id: str,
    req: ReplanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Trigger the automatic itinerary replanning workflow to handle weather changes, budget cuts, or schedule updates."""
    return await trip_service.replan_trip(db, trip_id, current_user.id, req)
